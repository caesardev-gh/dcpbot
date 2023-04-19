from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from bot.orm import models
from bot.bot_core import bot


class UserMiddleware(BaseMiddleware[Message]):

    def is_bot(self) -> bool:
        return self.event.from_id < 0

    async def pre(self):
        if self.is_bot():
            await self.stop()

        user, created = models.User.objects.get_or_create(
            user_id=self.event.from_id,
        )
        if created:
            api_user = (await bot.api.users.get(self.event.from_id))[0]
            user.first_name = api_user.first_name
            user.last_name = api_user.last_name
            user.save()
            self.cached = False
        else:
            self.cached = True

        self.send({"user": user})





