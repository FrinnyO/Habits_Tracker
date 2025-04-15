from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsSameUser
from .serializers import (TgChatIdSerializer, UserSerializer,
                          UserTokenObtainPairSerializer)
from .services import get_tg_chat_id


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSameUser,)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        user.last_login = timezone.now()
        user.save()
        return response


class TgChatIDRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TgChatIdSerializer

    def get_object(self):
        chat_id = self.request.user.tg_chat_id
        if chat_id:
            return User.objects.get(tg_chat_id=chat_id)
        user = User.objects.get(email=self.request.user.email)
        chat_id = get_tg_chat_id()
        if chat_id:
            user.tg_chat_id = chat_id
            user.save()
            return user
        raise NotFound(
            detail="Telegram ID not found. Please update your profile with your telegram_id."
        )
