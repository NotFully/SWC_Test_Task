document.addEventListener("DOMContentLoaded", function() {
    function updateMembers(eventId) {
    $.ajax({
        url: '/api/events/' + eventId + '/members/',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            var membersList = $('#members-list');
                membersList.empty();
                if (data.length === 0) {
                    membersList.append('<li>Нет участников</li>')
                }
                for (var i = 0; i < data.length; i++) {
                    membersList.append('<li><a href="/profile/' + data[i].id + '">' + data[i].first_name + ' ' + data[i].last_name + '</a></li>');
                }
        },
        error: function (error) {
            console.error(error);
        }
    });

    console.log('Обновление списка пользователей');
}

$('.event').each(function () {
    var eventId = $(this).data('event-id');
    setInterval(function () {
        updateMembers(eventId);
    }, 5000);
});
});

function updateEvents() {
    $.ajax({
        url: '/api/events/list/',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            var eventsList = $('#events-list');
            eventsList.empty();
            for (var i = 0; i < data.length; i++) {
                eventsList.append('<li><a href="/event/' + data[i].id + '">' + data[i].title + '</a></li>');
            }
        }
    });

    console.log('Обновление списка событий')
}

setInterval(updateEvents, 30000)
