from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Event


@receiver(pre_save, sender=Event)
def set_creator_if_not_specified(sender, instance, **kwargs):
    """
        Обработчик сигнала pre_save для модели Event.

        Если создатель события не указан, функция попытается установить
        создателя на основе текущего пользователя.

        Args:
            sender: Класс модели, отправивший сигнал (Event в данном случае).
            instance: Экземпляр модели Event, который будет сохранен.
            **kwargs: Дополнительные аргументы.

    """
    if not instance.creator:
        user_model = get_user_model()
        instance.creator = user_model.objects.get(pk=instance.user_id)
