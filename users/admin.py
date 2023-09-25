from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'birth_date', 'is_staff', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)
