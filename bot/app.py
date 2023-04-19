import os

from loguru import logger

from bot.bot_core import bot
from bot import middlewares
from bot import handlers


# Setup middleware

bot.labeler.message_view.register_middleware(middlewares.UserMiddleware)
bot.labeler.message_view.register_middleware(middlewares.MessageMiddleware)

# Register handlers

handlers.gpt.register_handlers(bot)


# Start polling

def start_polling():
    bot.run_forever()


if __name__ == "__main__":
    start_polling()
