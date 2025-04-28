from rest_framework import serializers

from .models import Habit
from .validators import validate_connected_habit_is_pleasant


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        habit = Habit(**data)
        if data.get("reward") and data.get("connected_habit"):
            raise serializers.ValidationError(
                "You cannot choose both a reward and a connected habit at the same time."
            )
        if (
            data.get("is_pleasant")
            and data.get("connected_habit")
            or data.get("reward")
        ):
            raise serializers.ValidationError(
                "Pleasant habit cannot have a connected habit or a reward."
            )
        validate_connected_habit_is_pleasant(habit)
        return data
