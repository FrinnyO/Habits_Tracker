from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="habits",
        verbose_name="Owner",
    )
    place = models.CharField(
        max_length=150, verbose_name="Place", null=True, blank=True
    )
    time = models.TimeField(verbose_name="Time", default="12:00")
    action = models.CharField(max_length=150, verbose_name="Action")
    is_pleasant = models.BooleanField(default=True, verbose_name="Is pleasant")
    connected_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="habits",
        verbose_name="Connected habit",
        null=True,
        blank=True,
    )
    periodicity_in_days = models.PositiveIntegerField(
        verbose_name="Periodicity in days",
        default=1,
        validators=[MaxValueValidator(7), MinValueValidator(1)],
    )
    last_scheduled = models.DateField(
        verbose_name="Last scheduled", null=True, blank=True
    )
    reward = models.CharField(
        max_length=150, verbose_name="Reward", null=True, blank=True
    )
    time_to_finish = models.PositiveIntegerField(
        verbose_name="Period",
        null=True,
        blank=True,
        validators=[MaxValueValidator(120)],
    )
    is_public = models.BooleanField(default=False, verbose_name="Is public")
