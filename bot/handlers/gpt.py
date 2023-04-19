import asyncio

from loguru import logger
from vkbottle.bot import Bot, Message

from bot.rules import GroupChatRule

from bot.danilgpt import DanilGPT

danil_gpt = DanilGPT()


async def type_forever(message: Message):
    while True:
        await message.ctx_api.messages.set_activity(peer_id=message.peer_id, type="typing")
        await asyncio.sleep(3)


async def gpt_handler(message: Message):
    typing_task = asyncio.create_task(type_forever(message))
    logger.info(f"Message from {message.peer_id}: {message.text}")
    try:
        response = await danil_gpt.get_response(
            chat_id=message.peer_id,
            user_id=message.from_id,
            text=message.text)
    except Exception as e:
        logger.error(e)
        response = "Я заебался постоянно отвечать тут на вопросы. Идите нахуй, сделайте без меня хоть что-то."
    finally:
        typing_task.cancel()
    await message.reply(response)


def register_handlers(bot: Bot):
    bot.on.private_message()(gpt_handler)
    bot.on.chat_message(GroupChatRule())(gpt_handler)
