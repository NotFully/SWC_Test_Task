from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Связываем форму с моделью CustomUser
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'password1', 'password2')
        # Указываем поля, которые будут отображаться на форме регистрации

    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )
