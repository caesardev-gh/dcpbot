from django.db import models


class Message(models.Model):
    class ROLE(models.TextChoices):
        SYSTEM = "system", "Система"
        ASSISTANT = "assistant", "Ассистент"
        USER = "user", "Пользователь"

    role = models.CharField(
        verbose_name="Роль",
        max_length=10,
        choices=ROLE.choices,
    )

    user = models.ForeignKey(
        "User",
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="messages",
    )

    chat_id = models.IntegerField(verbose_name="ID чата", null=False, blank=False)
    text = models.TextField(verbose_name="Текст", null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def to_json(self):
        return {
            "role": self.role,
            "content": self.text,
        }

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
