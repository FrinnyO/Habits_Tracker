from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        url = reverse("users:register")
        data = {"email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user(self):
        url = reverse("users:user-update", args=[self.user.pk])
        data = {"email": "test@example.com", "tg_chat_id": "12345"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.tg_chat_id, "12345")

    def test_retrieve_tg_chat_id(self):
        url = reverse("users:chat_id")

        # Simulate setting tg_chat_id
        self.user.tg_chat_id = "123456"
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tg_chat_id"], "123456")
