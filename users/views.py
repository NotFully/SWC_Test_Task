from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import RegistrationForm


class RegisterView(generics.CreateAPIView):
    """
        Регистрация нового пользователя.

        Создает нового пользователя на основе данных, полученных через API.
        Возвращает токен доступа (или создает новый, если пользователь уже существует) для нового пользователя.

        Параметры:
        - username: Имя пользователя
        - password: Пароль пользователя

        Возвращает:
        - token: Токен доступа пользователя
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class LoginView(generics.CreateAPIView):
    """
        Аутентификация пользователя.

        Проверяет переданные учетные данные (имя пользователя и пароль) и аутентифицирует пользователя.
        Возвращает токен доступа в случае успешной аутентификации.

        Параметры:
        - username: Имя пользователя
        - password: Пароль пользователя

        Возвращает:
        - token: Токен доступа пользователя
        - error (в случае неудачной аутентификации): Сообщение об ошибке
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=400)


class UserProfileView(generics.RetrieveAPIView):
    """
        Просмотр профиля пользователя.

        Возвращает данные профиля текущего аутентифицированного пользователя.

        Возвращает:
        - id: Идентификатор пользователя
        - username: Имя пользователя
        - email: Email пользователя
        - и другие поля профиля пользователя
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class registration(CreateView):
    """
        Страница регистрации пользователя.

        Отображает форму регистрации и обрабатывает запросы на создание нового пользователя.

        Параметры:
        - form_class: Класс формы для регистрации
        - success_url: URL-путь после успешной регистрации
        - template_name: Шаблон страницы регистрации
    """
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
