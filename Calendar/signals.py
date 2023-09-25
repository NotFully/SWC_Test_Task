from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Event


@receiver(pre_save, sender=Event)
def set_creator_if_not_specified(sender, instance, **kwargs):
    if not instance.creator:
        user_model = get_user_model()
        instance.creator = user_model.objects.get(pk=instance.user_id)
