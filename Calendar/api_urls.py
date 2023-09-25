from django.urls import path
from .views import EventCreateView, EventListView, EventJoinView, EventLeaveView, EventDeleteView

urlpatterns = [
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/list/', EventListView.as_view(), name='event-list'),
    path('events/join/<int:pk>/', EventJoinView.as_view(), name='event-join'),
    path('events/leave/<int:pk>/', EventLeaveView.as_view(), name='event-leave'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),
]
