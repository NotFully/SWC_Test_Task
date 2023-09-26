from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    """
        Класс настройки административной панели для модели Event.

        Attributes:
            list_display (tuple): Список полей, отображаемых в списке событий.
            list_filter (tuple): Список полей, по которым можно фильтровать события.
            search_fields (tuple): Поля, по которым можно выполнять поиск событий.
            filter_horizontal (tuple): Список полей, которые отображаются как множественный выбор в административной панели.
    """
    list_display = ('title', 'date_creation', 'creator')
    list_filter = ('date_creation', 'creator')
    search_fields = ('title', 'creator__username')
    filter_horizontal = ('members',)


# Регистрируем модель Event и связываем ее с настройками EventAdmin
admin.site.register(Event, EventAdmin)
