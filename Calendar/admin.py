from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_creation', 'creator')
    list_filter = ('date_creation', 'creator')
    search_fields = ('title', 'creator__username')
    filter_horizontal = ('members',)


admin.site.register(Event, EventAdmin)
