from django.db import models


class User(models.Model):
    user_id = models.IntegerField(verbose_name="ID пользователя", unique=True, editable=False)
    username = models.CharField(max_length=255, verbose_name="Имя пользователя", null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")

    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    last_seen = models.DateTimeField(auto_now=True, verbose_name="Последний визит")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.user_id}"

    def to_json(self):
        return {
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "link": self.link,
            "joined_at": self.joined_at.strftime("%d.%m.%Y %H:%M:%S"),
            "last_seen": self.last_seen.strftime("%d.%m.%Y %H:%M:%S"),
        }

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name

    @property
    def link(self) -> str:
        return f"https://vk.com/{self.username}" if self.username else f"https://vk.com/id{self.user_id}"

