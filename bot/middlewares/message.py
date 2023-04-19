from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from bot.orm import models


class MessageMiddleware(BaseMiddleware[Message]):
    def is_bot(self) -> bool:
        return self.event.from_id < 0

    async def pre(self):
        if self.is_bot():
            await self.stop()

        message = models.Message.objects.create(
            role=models.Message.ROLE.USER,
            user=models.User.objects.get(user_id=self.event.from_id),
            chat_id=self.event.peer_id,
            text=self.event.text,
        )
        message.save()

