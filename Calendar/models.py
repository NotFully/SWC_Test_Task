from django.db import models
from django.conf import settings


class Event(models.Model):
    """
        Модель для представления событий.

        Attributes:
            title (CharField): Название события (максимум 255 символов).
            text (TextField): Текстовое описание события.
            date_creation (DateTimeField): Дата и время создания события (автоматически заполняется).
            creator (ForeignKey): Внешний ключ для создателя события (ссылается на модель пользователя).
            members (ManyToManyField): Множество пользователей, участвующих в событии.

        Methods:
            __str__(): Возвращает строковое представление события (его название).

            save(*args, **kwargs): Переопределенный метод сохранения события, который автоматически
            устанавливает создателя события, если он не указан.

    """
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        default=None
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participation_in_events')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
            Переопределенный метод сохранения события.

            Если создатель события не указан, метод попытается установить
            создателя на основе текущего пользователя.

            Args:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

        """
        if not self.creator:
            self.creator = settings.AUTH_USER_MODEL.objects.get(pk=self.user_id)
        super(Event, self).save(*args, **kwargs)
