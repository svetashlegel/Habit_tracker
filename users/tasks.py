from celery import shared_task

from users.models import User
from users.services import tg_get_updates, tg_send_message


@shared_task(name="get_tg_chat_id")
def get_tg_chat_id():
    tg_data = tg_get_updates()
    users = User.objects.filter(chat_id=None)
    if tg_data['ok'] and tg_data['result'] != []:
        for message in tg_data['result']:
            if message['message']['text'] == "/start":
                for user in users:
                    if user.telegram_user_name.lower() == message['message']['from']['username'].lower():
                        user.chat_id = message['message']['from']['id']
                        user.save()
                        tg_get_updates(message['update_id'])
                        text = f'Добро пожаловать! Сюда будут приходить напоминания о ваших привычках!'
                        tg_send_message(user.chat_id, text)
            tg_get_updates(message['update_id'])
