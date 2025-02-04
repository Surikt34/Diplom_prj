from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

from .tasks import send_welcome_email

User = get_user_model()

class RegisterView(GenericAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Создать нового пользователя и отправить приветственное письмо.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_welcome_email.delay(user.email)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(RetrieveUpdateAPIView):
    """
    Эндпоинт для получения и обновления профиля пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """
        Возвращает текущего пользователя.
        """
        return self.request.user

