from django.db import models
from django.conf import settings


class Event(models.Model):
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
        if not self.creator:
            self.creator = settings.AUTH_USER_MODEL.objects.get(pk=self.user_id)
        super(Event, self).save(*args, **kwargs)
