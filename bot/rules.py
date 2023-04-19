from vkbottle.dispatch.rules.base import ABCRule, BaseMessageMin


class GroupChatRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return self.is_for_me(event)

    @staticmethod
    def is_for_me(event: BaseMessageMin) -> bool:
        name_list = [
            "данил",
            "денчик",
            "даня",
        ]

        mention = any([name in event.text.lower() for name in name_list])

        reply = False
        if event.reply_message:
            if event.reply_message.from_id == -219891628:
                reply = True

        return mention or reply
