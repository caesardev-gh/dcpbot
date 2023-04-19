import os
import time
import multiprocessing

import watchdog.events
import watchdog.observers
from loguru import logger

from bot.app import start_polling
from bot.orm import settings

logger.add(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/logs/.log",
    rotation="500 MB",
    compression="zip",
)


class Handler(watchdog.events.PatternMatchingEventHandler):
    """
    A class to handle file system events in a specified directory and restart a bot application upon detecting changes.

    Attributes:
    - bot_polling_process (multiprocessing.Process): A multiprocessing process to run the bot application.
    - stat (os.stat_result): The stat result of the last processed file.

    Methods:
    - reload_bot(): Terminate the current bot polling process and start a new one.
    - on_created(event): Restart the bot application if a new file is created.
    - on_modified(event): Restart the bot application if an existing file is modified.
    """

    def __init__(self):
        super().__init__(ignore_directories=True, case_sensitive=True, patterns=['*.py'], ignore_patterns=[__file__])
        self.bot_polling_process = multiprocessing.Process(target=start_polling)
        self.bot_polling_process.start()
        self.stat = None

    def reload_bot(self):
        """
        Terminate the current bot polling process and start a new one.

        :return: None
        """
        self.bot_polling_process.terminate()
        self.bot_polling_process = multiprocessing.Process(target=start_polling)
        self.bot_polling_process.start()

    def on_created(self, event):
        """
        Restart the bot application if a new file is created.

        :param (watchdog.events.FileCreatedEvent) event: The event object representing the created file.
        :return: None
        """
        if self.stat == (file_stat := os.stat(event.src_path)):
            return
        self.stat = file_stat
        logger.info(f"New file created - {event.src_path}. Reloading...")
        self.reload_bot()

    def on_modified(self, event):
        """
        Restart the bot application if an existing file is modified.

        :param (watchdog.events.FileModifiedEvent) event: The event object representing the modified file.
        :return: None
        """
        if self.stat == (file_stat := os.stat(event.src_path)):
            return
        self.stat = file_stat
        logger.info(f"The file was modified - {event.src_path}. Reloading...")
        self.reload_bot()


def start_reload_polling():
    """
    Start the watchdog observer to monitor the specified directory for file changes and restart the bot application
    upon detecting changes.
    """
    observer, event_handler = watchdog.observers.Observer(), Handler()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(__file__)), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    event_handler.bot_polling_process.terminate()
    observer.join()


def run_bot():
    """
    Start the bot application by calling the appropriate function based on the DEBUG flag in the settings module.
    """
    if settings.DEBUG:
        start_reload_polling()
    else:
        start_polling()


if __name__ == "__main__":
    run_bot()
