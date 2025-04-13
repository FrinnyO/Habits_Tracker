from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "password", "tg_chat_id"]


class TgChatIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "tg_chat_id"]


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["password"] = user.password

        return token
