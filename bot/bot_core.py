import os

from dotenv import load_dotenv
from vkbottle.bot import Bot

load_dotenv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/.env")

bot = Bot(os.getenv("BOT_TOKEN"))
