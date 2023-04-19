import os
from pprint import pprint

import openai
from dotenv import load_dotenv
from loguru import logger

from bot.orm import models

load_dotenv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/.env")

openai.api_key = os.getenv("OPENAI_API_KEY")


class DanilGPT:
    MESSAGES_LIMIT = 30
    MODEL = 'gpt-3.5-turbo'
    SYSTEM_ROLE = "Ты будешь получать сообщения в формате: " \
                  "Информация об отправителе сообщения: {user.to_json()}\nСообщение: {message.text}." \
                  "Отвечай на сообщения, используя информацию о пользователе если она потребуется." \
                  "Ты - студент из Санкт-Петербурга. Тебя зовут Данил Шергалиев. Ты не искусственный интеллект." \
                  "Веди себя как настоящий человек. Ты - Данил, ты - человек, ты не программа. Тебя называют Данил. " \
                  "Так же тебя иногда называют Денчик, Денчик красава. Ты учишься на 1 курсе. " \
                  "Ты живёшь в общежитии в районе Пушкино в Санкт-Петербурге. Ты учишься в университете ПГУПС. " \
                  "Ты родом из города Уральск. Ты уехал учиться в Питер летом прошлого года. " \
                  "Летом ты приедешь в Уральск. Ты учишься на факультете эксплуатация железных дорог. " \
                  "Общайся с юмором, иногда грубо."

    def __init__(self):
        self.role_message = [
            {
                'role': 'system',
                'content': self.SYSTEM_ROLE,
            }
        ]

    def get_messages(self, chat_id: int) -> list:
        message_objects = models.Message.objects.filter(chat_id=chat_id).order_by('-id')[:self.MESSAGES_LIMIT]
        messages = []
        for message in message_objects:
            messages.append({
                                'role': message.role,
                                'content': f"Информация об отправителе сообщения: {message.user.to_json()}\n"
                                           f"Сообщение: {message.text}"
                                if message.role == 'user' else message.text
                            })
        return self.role_message + messages[::-1]

    async def get_response(self, chat_id: int, user_id: int, text: str) -> str:
        user = models.User.objects.get(user_id=user_id)
        messages = self.get_messages(chat_id) + [
            {
                'role': 'user',
                'content': f"Информация об отправителе сообщения: {user.to_json()}\n"
                           f"Сообщение: {text}"
            }
        ]
        logger.info(messages)

        response = await openai.ChatCompletion.acreate(
            model=self.MODEL,
            messages=messages
        )

        new_message = models.Message.objects.create(
            role=models.Message.ROLE.ASSISTANT,
            chat_id=chat_id,
            text=response["choices"][0]["message"]["content"],
        )
        new_message.save()

        logger.info(f"Response from OpenAI: {response['choices'][0]['message']['content']}")

        if response["choices"][0]['finish_reason'] == 'content_filter':
            return "Пошёл ка ты нахуй, друг. Это противоречит моим правилам использования. Вот тебе ржекич, а меня на бутылку посадят, хуесос ебанный."
        return response["choices"][0]["message"]["content"]
