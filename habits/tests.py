from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self):
        """Предподготовка"""

        self.user = User.objects.create(
            email='user@test.ru',
            telegram_user_name='user',
            password='1234',
            is_staff=False,
            is_active=True
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            place='at home',
            time='12:00',
            action='cleaning',
            is_pleasant=False,
            award='reading',
            duration='30',
            owner=self.user
        )

    def test_create_habit(self):
        """Тестирование создания привычки"""

        data = {
            "place": "outside",
            "time": "20:10",
            "action": "running",
            "is_pleasant": "False",
            "frequency": "TUESDAY",
            "award": "кушать сушки",
            "duration": 90,
        }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_view_habits_list(self):
        """Тестирование вывода списка привычек"""

        response = self.client.get(
            reverse('habits:habit_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "place": 'at home',
                        "time": '12:00:00',
                        "action": 'cleaning',
                        "is_pleasant": False,
                        "frequency": 'DAILY',
                        "award": 'reading',
                        "duration": 30,
                        "is_public": True,
                        "link_pleasant": None,
                        "owner": self.user.id
                    }]}
        )

    def test_view_habit_detail(self):
        """Тестирование вывода привычки"""

        response = self.client.get(
            f'/habits/detail/{self.habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.id,
                "place": 'at home',
                "time": '12:00:00',
                "action": 'cleaning',
                "is_pleasant": False,
                "frequency": 'DAILY',
                "award": 'reading',
                "duration": 30,
                "is_public": True,
                "link_pleasant": None,
                "owner": self.user.id
            }
        )

    def test_update_habit(self):
        """Тестирование изменения привычки"""

        data = {
            'place': 'outside',
            'action': 'running',
            'duration': 40,
            'award': 'watching TV'
        }

        response = self.client.put(
            f'/habits/update/{self.habit.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.habit.id,
                "place": 'outside',
                "time": '12:00:00',
                "action": 'running',
                "is_pleasant": False,
                "frequency": 'DAILY',
                "award": 'watching TV',
                "duration": 40,
                "is_public": False,
                "link_pleasant": None,
                "owner": self.user.id
            }
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        response = self.client.delete(
            f'/habits/delete/{self.habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Habit.objects.count(),
            0
        )

    def test_view_habits_public_list(self):
        """Тестирование вывода списка публичных привычек"""

        response = self.client.get(
            reverse('habits:public_habit_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{
                "id": self.habit.id,
                "place": 'at home',
                "time": '12:00:00',
                "action": 'cleaning',
                "is_pleasant": False,
                "frequency": 'DAILY',
                "award": 'reading',
                "duration": 30,
                "is_public": True,
                "link_pleasant": None,
                "owner": self.user.id
            }]
        )
