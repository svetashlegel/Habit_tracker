from datetime import datetime
from habits.models import Habit
from users.services import tg_send_message
from celery import shared_task


@shared_task(name="send_habits")
def send_habits():
    current_time = datetime.now()
    today = datetime.today().strftime('%A')
    for habit in Habit.objects.filter(is_pleasant=False):
        if habit.frequency == "Daily" or habit.frequency == today:
            if habit.time.strftime("%H:%M") == current_time.strftime("%H:%M"):
                chat_id = habit.owner.chat_id
                if habit.award:
                    users_award = habit.award
                else:
                    users_award = habit.link_pleasant.action
                message = (f"Трекер полезных привычек. Напоминание.\nДействие: {habit.action}\nМесто: {habit.place}"
                           f"\nПродолжительность: {habit.duration} мин.\nВаше вознаграждение: {users_award}")
                tg_send_message(chat_id, message)
