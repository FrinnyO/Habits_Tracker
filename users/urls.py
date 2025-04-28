from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig

from .views import (TgChatIDRetrieveAPIView, UserCreateAPIView,
                    UserTokenObtainPairView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", UserTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("chat_id/", TgChatIDRetrieveAPIView.as_view(), name="chat_id"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
]
