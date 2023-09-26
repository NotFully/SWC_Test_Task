from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
        Менеджер пользователей для модели CustomUser.
        Менеджер для создавания пользователей и суперпользователей.
    """
    def create_user(self, username, password=None, **extra_fields):
        """
            Создает и сохраняет нового пользователя.

            Args:
                username (str): Имя пользователя.
                password (str, optional): Пароль пользователя. Может быть None при создании.
                **extra_fields: Дополнительные поля пользователя.

            Returns:
                CustomUser: Новый созданный пользователь.
        """
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
            Создает и сохраняет нового суперпользователя.

            Args:
                username (str): Имя суперпользователя.
                password (str, optional): Пароль суперпользователя. Может быть None при создании.
                **extra_fields: Дополнительные поля суперпользователя.

            Returns:
                CustomUser: Новый созданный суперпользователь.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        Пользовательская модель CustomUser.

        Attributes:
            id (int): Уникальный идентификатор пользователя.
            username (str): Имя пользователя.
            first_name (str): Имя пользователя.
            last_name (str): Фамилия пользователя.
            date_joined (datetime): Дата и время регистрации пользователя.
            birth_date (date, optional): Дата рождения пользователя (может быть None).

            is_active (bool): Флаг активности пользователя.
            is_staff (bool): Флаг сотрудника. True для суперпользователей.
            is_superuser (bool): Флаг суперпользователя.

        Methods:
            has_module_perms(app_label): Проверяет разрешения на модуль.
            has_perm(perm, obj=None): Проверяет разрешения.
            get_short_name(): Возвращает короткое имя пользователя.
            get_full_name(): Возвращает полное имя пользователя.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
