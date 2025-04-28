from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram chat ID"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default_avatar.jpg",
        blank=True,
        null=True,
        verbose_name="Avatar",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "email",
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
