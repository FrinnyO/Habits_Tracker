from django.core.exceptions import ValidationError


def validate_connected_habit_is_pleasant(habit):
    if habit.connected_habit and not habit.connected_habit.is_pleasant:
        raise ValidationError("The connected habit must be pleasant.")
