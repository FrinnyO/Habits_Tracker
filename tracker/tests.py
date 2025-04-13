from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import Habit
from tracker.services import send_tg_message
from users.models import User


class SendTgMessageServiceTests(TestCase):

    @patch("tracker.services.requests.get")
    def test_send_tg_message(self, mock_get):
        send_tg_message("Test message", "123456")
        mock_get.assert_called_once_with(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params={"text": "Test message", "chat_id": "123456"},
        )


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test1@mail.com")
        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            action="jump 20 times",
            place="Gym",
            time_to_finish=100,
            periodicity_in_days=2,
            is_pleasant=True,
            is_public=True,
        )
        self.unpleasant_habit = Habit.objects.create(
            owner=self.user,
            action="jump 20 times",
            place="Gym",
            time_to_finish=100,
            periodicity_in_days=2,
            is_pleasant=False,
        )

    def test_create_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-create")
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 100,
            "periodicity_in_days": 2,
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_create_habit_min_max_validators_error(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-create")
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 100,
            "periodicity_in_days": 8,
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 2)
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 130,
            "periodicity_in_days": 4,
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 2)
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 10,
            "periodicity_in_days": 0,
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_connected_habit_is_pleasant(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-create")
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 100,
            "periodicity_in_days": 6,
            "connected_habit": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 100,
            "periodicity_in_days": 6,
            "connected_habit": 2,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 3)

    def test_create_pleasant_habit_with_reward(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-create")
        data = {
            "is_public": True,
            "action": "jump 10 times",
            "place": "Gym",
            "time_to_finish": 100,
            "periodicity_in_days": 6,
            "reward": "chocolate",
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_public_list_habits(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:public-habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-update", args=[self.pleasant_habit.pk])
        data = {
            "is_public": True,
            "action": "jump 30 times",
            "place": "Home",
            "time_to_finish": 50,
            "periodicity_in_days": 3,
            "is_pleasant": True,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Habit.objects.get(id=self.pleasant_habit.pk).action, "jump 30 times"
        )

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:habit-delete", args=[self.pleasant_habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)
