from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from .serializers import EventSerializer
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from .forms import EventForm


class EventCreateView(generics.CreateAPIView):
    """
        Представление для создания нового события.

        Атрибуты:
            queryset (QuerySet): Запрос к модели Event для получения списка всех событий.
            serializer_class (Serializer): Сериализатор, используемый для создания события.
            permission_classes (list): Список классов разрешений, позволяющих только
                                       аутентифицированным пользователям создавать события.

        Методы:
            perform_create(serializer): Вызывается для сохранения события с указанным создателем.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
                Сохраняет событие с указанным создателем.

            Args:
                serializer (EventSerializer): Сериализатор для события.

            Returns:
                Response: JSON-ответ с созданным событием и кодом статуса.

            """
        serializer.save(creator=self.request.user)


class EventListView(generics.ListAPIView):
    """
        Представление для получения списка всех событий.

        Attributes:
            queryset (QuerySet): Запрос к модели Event для получения списка всех событий.
            serializer_class (Serializer): Сериализатор для событий.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventJoinView(generics.UpdateAPIView):
    """
        Представление для присоединения к событию.

        Attributes:
            queryset (QuerySet): Запрос к модели Event для получения списка всех событий.
            serializer_class (Serializer): Сериализатор для событий.
            permission_classes (list): Список классов разрешений, позволяющих только
                                       аутентифицированным пользователям присоединяться к событиям.

        Methods:
            update(request, *args, **kwargs): Обрабатывает запрос на присоединение к событию.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
            Обрабатывает запрос на присоединение к событию.

            Args:
                request (Request): Запрос, содержащий информацию о пользователе и событии.
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Returns:
                Response: JSON-ответ с сообщением о присоединении или ошибкой, если пользователь уже участвует в событии.

        """
        event = self.get_object()
        user = request.user
        if user not in event.members.all():
            event.members.add(user)
            return Response({"message": "Вы присоединились к событию"})
        else:
            return Response({"error": "Вы уже участвуете в этом событии"}, status=status.HTTP_400_BAD_REQUEST)


class EventLeaveView(generics.UpdateAPIView):
    """
        Представление для покидания события.

        Attributes:
            queryset (QuerySet): Запрос к модели Event для получения списка всех событий.
            serializer_class (Serializer): Сериализатор для событий.
            permission_classes (list): Список классов разрешений, позволяющих только
                                       аутентифицированным пользователям покидать события.

        Methods:
            update(request, *args, **kwargs): Обрабатывает запрос на покидание события.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
            Обрабатывает запрос на покидание события.

            Args:
                request (Request): Запрос, содержащий информацию о пользователе и событии.
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Returns:
                Response: JSON-ответ с сообщением о покидании или ошибкой, если пользователь не участвует в событии.

        """
        event = self.get_object()
        user = request.user
        if user in event.members.all():
            event.members.remove(user)
            return Response({"message": "Вы покинули событие"})
        else:
            return Response({"error": "Вы не участвуете в этом событии"}, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteView(generics.DestroyAPIView):
    """
        Представление для удаления события.

        Attributes:
            queryset (QuerySet): Запрос к модели Event для получения списка всех событий.
            serializer_class (Serializer): Сериализатор для событий.
            permission_classes (list): Список классов разрешений, позволяющих только
                                       создателю события удалять его.

        Methods:
            destroy(request, *args, **kwargs): Обрабатывает запрос на удаление события.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
            Обрабатывает запрос на удаление события.

            Args:
                request (Request): Запрос, содержащий информацию о пользователе и событии.
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.

            Returns:
                Response: JSON-ответ с сообщением об успешном удалении или ошибкой, если пользователь не создатель события.

            """
        event = self.get_object()
        if event.creator == request.user:
            event.delete()
            return Response({"message": "Событие успешно удалено"})
        else:
            return Response({"error": "У вас нет прав для удаления этого события"}, status=status.HTTP_403_FORBIDDEN)


class EventMembersListView(generics.ListAPIView):
    """
        Представление для получения списка участников события.

        Attributes:
            serializer_class (Serializer): Сериализатор для пользователей, участвующих в событии.

        Methods:
            get_queryset(): Возвращает список пользователей, участвующих в указанном событии.

    """
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        """
            Возвращает список пользователей, участвующих в указанном событии.

            Returns:
                QuerySet: Список пользователей.

            """
        event_id = self.kwargs['event_id']
        return CustomUser.objects.filter(participation_in_events__id=event_id)


def event_list(request):
    """
        Представление для отображения списка всех событий.

        Args:
            request (HttpRequest): Запрос от клиента.

        Returns:
            HttpResponse: HTML-страница со списком событий.

    """
    if request.user.is_authenticated:
        events = Event.objects.all()
        participating_events = request.user.participation_in_events.all()
        return render(request, 'main/index.html', {'events': events, 'participating_events': participating_events})
    else:
        events = Event.objects.all()
        return render(request, 'main/index.html', {'events': events})


def user_profile(request, user_id):
    """
        Представление для отображения профиля пользователя.

        Args:
            request (HttpRequest): Запрос от клиента.
            user_id (int): Идентификатор пользователя.

        Returns:
            HttpResponse: HTML-страница профиля пользователя.

    """
    user = get_object_or_404(CustomUser, id=user_id)
    events = Event.objects.all()
    created_events = Event.objects.filter(creator=user)
    participating_events = user.participation_in_events.all()

    return render(request, 'users/profile.html', {
        'user': user,
        'events': events,
        'created_events': created_events,
        'participating_events': participating_events,
    })


def event_detail(request, event_id):
    """
        Представление для отображения подробной информации о событии.

        Args:
            request (HttpRequest): Запрос от клиента.
            event_id (int): Идентификатор события.

        Returns:
            HttpResponse: HTML-страница с подробной информацией о событии.

    """
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all()
    if request.user.is_authenticated:
        participating_events = request.user.participation_in_events.all()
        return render(request, 'events/event_detail.html',
                      {'event': event, 'events': events, 'participating_events': participating_events})
    else:
        events = Event.objects.all()
        return render(request, 'events/event_detail.html', {'event': event, 'events': events})


def join_event(request, event_id):
    """
        Представление для присоединения пользователя к событию.

        Args:
            request (HttpRequest): Запрос от клиента.
            event_id (int): Идентификатор события.

        Returns:
            HttpResponse: Перенаправление на страницу с подробной информацией о событии.

    """
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.members.all():
        event.members.add(request.user)
    event_detail(request, event_id)
    return redirect('Calendar:event_detail', event_id=event.id)


def leave_event(request, event_id):
    """
        Представление для покидания пользователем события.

        Args:
            request (HttpRequest): Запрос от клиента.
            event_id (int): Идентификатор события.

        Returns:
            HttpResponse: Перенаправление на страницу с подробной информацией о событии.

    """
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.members.all():
        event.members.remove(request.user)
    event_detail(request, event_id)
    return redirect('Calendar:event_detail', event_id=event.id)


def delete_event(request, event_id):
    """
        Представление для удаления события пользователем.

        Args:
            request (HttpRequest): Запрос от клиента.
            event_id (int): Идентификатор события.

        Returns:
            HttpResponse: Перенаправление на страницу со списком событий.

    """
    event = get_object_or_404(Event, id=event_id)
    if request.user == event.creator:
        event.delete()
    return redirect('Calendar:index')


def create_event(request):
    """
        Представление для создания нового события.

        Args:
            request (HttpRequest): Запрос от клиента.

        Returns:
            HttpResponse: HTML-страница для создания события или перенаправление на страницу с подробной информацией о событии.

    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('Calendar:event_detail', event_id=event.id)
    else:
        form = EventForm()
    events = Event.objects.all()
    participating_events = request.user.participation_in_events.all()
    return render(request, 'events/create_event.html', {'form': form, 'events': events, 'participating_events': participating_events})
