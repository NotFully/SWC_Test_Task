from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from .serializers import EventSerializer
from users.models import CustomUser


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventJoinView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        if user not in event.members.all():
            event.members.add(user)
            return Response({"message": "Вы присоединились к событию"})
        else:
            return Response({"error": "Вы уже участвуете в этом событии"}, status=status.HTTP_400_BAD_REQUEST)


class EventLeaveView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        if user in event.members.all():
            event.members.remove(user)
            return Response({"message": "Вы покинули событие"})
        else:
            return Response({"error": "Вы не участвуете в этом событии"}, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.creator == request.user:
            event.delete()
            return Response({"message": "Событие успешно удалено"})
        else:
            return Response({"error": "У вас нет прав для удаления этого события"}, status=status.HTTP_403_FORBIDDEN)


def event_list(request):
    events = Event.objects.all()
    return render(request, 'main/index.html', {'events': events})


def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    created_events = Event.objects.filter(creator=user)
    participating_events = user.participation_in_events.all()

    return render(request, 'users/profile.html', {
        'user': user,
        'created_events': created_events,
        'participating_events': participating_events,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.members.all():
        event.members.add(request.user)
    return render(request, 'events/event_detail.html', {'event': event})


def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.members.all():
        event.members.remove(request.user)
    return render(request, 'events/event_detail.html', {'event': event})
