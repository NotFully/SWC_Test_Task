from django.urls import path
from . import views
from django.contrib.auth.views import *

app_name = 'Calendar'

urlpatterns = [
    path('index', views.event_list, name='index'),
    path('profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('event_detail/<int:event_id>', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/join', views.join_event, name='join_event'),
    path('event/<int:event_id>/leave', views.leave_event, name='leave_event'),
]
