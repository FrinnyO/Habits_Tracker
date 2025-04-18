from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "password", "tg_chat_id"]

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user= User(
            email = validated_data["email"],
            avatar = validated_data.get["avatar", None],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


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
