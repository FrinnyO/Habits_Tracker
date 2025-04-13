from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "owner",
        "place",
        "time",
        "is_pleasant",
        "connected_habit",
        "periodicity_in_days",
        "reward",
        "time_to_finish",
        "is_public",
    )
