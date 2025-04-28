from celery import shared_task
from django.utils import timezone

from users.models import User

from .services import send_tg_message


@shared_task
def send_habit_notification():
    all_users = User.objects.all()
    for user in all_users:
        habit_counter = 0
        if user.tg_chat_id:
            chat_id = user.tg_chat_id
            user_habits = user.habits.all()
            if user_habits:
                hello_text = f"Hello, {user.email}! Here is overview of your habits!"
            else:
                hello_text = f"Hello, {user.email}! You have no habits yet. Create them in the app!"
            send_tg_message(hello_text, chat_id)
            for habit in user_habits:
                habit_counter += 1
                last_scheduled = habit.last_scheduled or timezone.now()
                habit.last_scheduled = last_scheduled
                habit.save()
                next_schedule = last_scheduled + timezone.timedelta(
                    days=habit.periodicity_in_days
                )
                additional_text = ""
                if habit.connected_habit:
                    additional_text += (
                        f"First complete {habit.connected_habit.action} habit too!\n"
                    )
                if habit.is_pleasant:
                    additional_text += "Don't forget to enjoy it!\n"
                if habit.reward:
                    additional_text += f"Your reward will be {habit.reward}.\n"
                text = f"""
                Habit #{habit_counter}: 
                {habit.time}
                {habit.action} at {habit.place}!
                You need {habit.time_to_finish} seconds to finish it.
                {additional_text}
                Last scheduled: {last_scheduled}.
                Next schedule: {next_schedule}.
                """
                send_tg_message(text, chat_id)
