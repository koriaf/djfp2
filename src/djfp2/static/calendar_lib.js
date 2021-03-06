PlannerLib = {};
PlannerLib.calendar = {};
PlannerLib.calendar.popup = {};

PlannerLib.calendar.eventCreate = function(new_event) {
    $.post(
        "/calendar/events/create/",
        {
            'title': new_event.title,
            'start_date': new_event.start.toISOString(),
            'end_date': new_event.end.toISOString(),
            'event_to_replace': new_event.id,
            'color': new_event.backgroundColor,
            'textcolor': new_event.textColor,
        },
        function(created_event) {
            if (created_event.result != 'success') {
                alert(JSON.stringify(created_event.message));
                $("#calendar").fullCalendar('removeEvents', new_event.id);
            }
            else {
                $("#calendar").fullCalendar('removeEvents', created_event.event_to_replace);
                $("#calendar").fullCalendar('renderEvent', created_event);
            }
        }
    ).fail(function(data) {
        alert(JSON.stringify(data));
    });
}

PlannerLib.calendar.eventSave = function(new_event) {
    $.post(
        "/calendar/events/update/",
        {
            'event_id': new_event.id,
            'start_date': new_event.start.toISOString(),
            'end_date': new_event.end.toISOString(),
            'title': new_event.title,
            'color': new_event.backgroundColor,
            'textcolor': new_event.textColor,
            'is_notify': new_event.is_notify
        },
        function(data) {
            if (data.result != "success") {
                alert(JSON.stringify(data));
            }
        }
    ).fail(function(data) {
        alert(JSON.stringify(data));
    });
}

PlannerLib.calendar.eventRender = function(event, element, view) {
    if (event.is_notify) {
        element.find(".fc-title").css("font-weight", "bold")
    }
}

PlannerLib.calendar.eventRemove = function(event_id) {
    $.post(
        "/calendar/events/remove/",
        {
            'event_id': event_id,
        },
        function(data) {
            if (data.result != "success") {
                alert(JSON.stringify(data));
            }
        }
    ).fail(function(data) {
        alert(JSON.stringify(data));
    });
}

PlannerLib.calendar.eventClick = function(calEvent, view) {
    var $popup = $("#popup");

    // set position
    var e = view;
    var top = e.pageY - 100;
    var left = e.pageX - 200;
    top = Math.max(top, 0);
    left = Math.max(left, 0);
    $popup.css('top', top);
    $popup.css('left', left);
    // fill form fields by initial values
    // using find() here determines right DOM (id_event_id will be always child for popup, and so on)
    $popup.find("#id_event_id").val(calEvent.id);
    $popup.find("#id_event_title").val(calEvent.title);
    $popup.find("#id_notify_me").attr('checked', calEvent.is_notify);
    $popup.show();
    $popup.find("#id_event_title").focus();
}


PlannerLib.calendar.eventChange = function(event, delta, revertFunc, jsEvent, ui, view)
{
    var new_event = $("#calendar").fullCalendar('clientEvents', event.id)[0];
    PlannerLib.calendar.eventSave(new_event);
}


PlannerLib.calendar.dayClick = function(date, jsEvent, view) {
    new_event_id = new Date().getTime();
    end = moment(date).add(1, 'h');
    new_event = {
        title: 'New event',
        start: date,
        end: end,
        id: new_event_id,
    };
    $("#calendar").fullCalendar('renderEvent', new_event);
    var new_event = $("#calendar").fullCalendar('clientEvents', new_event_id)[0];
    PlannerLib.calendar.eventCreate(new_event);
}


PlannerLib.calendar.eventColorChange = function() {
    var $th = $(this);
    var $popup = $("#popup");
    var bgcolor = $th.css('background-color');
    var textcolor = $th.css('color');
    var event_id = $('#popup #id_event_id').val();
    var event_notify = $("#popup #id_notify_me")[0].checked;

    var current_event = $("#calendar").fullCalendar('clientEvents', event_id)[0];
    current_event.backgroundColor = bgcolor;
    current_event.textColor = textcolor;
    current_event.is_notify = event_notify;
    $("#calendar").fullCalendar('updateEvent', current_event);

    $("#popup").hide();
    PlannerLib.calendar.eventSave(current_event);
    return false;
}

PlannerLib.calendar.popup.pressSaveButton = function() {
    var $popup = $("#popup");
    var event_id = parseInt($popup.find("#id_event_id").val());
    var event_title = $popup.find("#id_event_title").val();
    var event_notify = $popup.find("#id_notify_me")[0].checked;

    var calEvent = $("#calendar").fullCalendar('clientEvents', event_id)[0];

    calEvent.title = event_title;
    calEvent.is_notify = event_notify;
    $("#calendar").fullCalendar('updateEvent', calEvent);

    PlannerLib.calendar.eventSave(calEvent);
    $popup.hide();
    return false;
}

PlannerLib.calendar.popup.pressDeleteButton = function() {
    var $popup = $("#popup");
    var event_id = parseInt($popup.find("#id_event_id").val());
    $("#calendar").fullCalendar('removeEvents', event_id);
    PlannerLib.calendar.eventRemove(event_id);
    $popup.hide();
    return false;
}


PlannerLib.calendar.setTimeline = function(view) {
    var height = window.innerHeight - 50;
    $('#calendar').fullCalendar('option', 'height', height);
    var parentDiv = $('.fc-slats:visible').parent();
    var timeline = parentDiv.children(".timeline");
    if (timeline.length == 0) { //if timeline isn't there, add it
        timeline = $("<hr>").addClass("timeline");
        parentDiv.prepend(timeline);
    }

    var curTime = new Date();

    var curCalView = $("#calendar").fullCalendar('getView');
    if (curCalView.intervalStart < curTime && curCalView.intervalEnd > curTime) {
        timeline.show();
    } else {
        timeline.hide();
        return;
    }
    var calMinTimeInMinutes = strTimeToMinutes(curCalView.opt("minTime"));
    var calMaxTimeInMinutes = strTimeToMinutes(curCalView.opt("maxTime"));

    var curMinutes = curTime.getHours() * 60 + curTime.getMinutes();
    var relMinutes = curMinutes - calMinTimeInMinutes;
    var percentOfDay = relMinutes / (calMaxTimeInMinutes - calMinTimeInMinutes);

    var topLoc = Math.floor($("div.fc-slats").height() * percentOfDay);

    var timeCol = $('.fc-time:visible');
    timeline.css({top: topLoc + "px", left: (timeCol.outerWidth(true))+"px"});

    if (curCalView.name == "agendaWeek") { //week view, don't want the timeline to go the whole way across
        var dayCol = $(".fc-today:visible");
        var left = dayCol.position().left;
        var width = dayCol.width();
        timeline.css({left: left + "px", width: width + "px"});
    }
}

/* misc */
function strTimeToMinutes(str_time) {
    var arr_time = str_time.split(":");
    var hour = parseInt(arr_time[0]);
    var minutes = parseInt(arr_time[1]);
    return((hour * 60) + minutes);
}

function rgb2hex(rgb) {
    rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    function hex(x) {
        return ("0" + parseInt(x).toString(16)).slice(-2);
    }
    return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
}

function isAnythingToNotify() {
    /* periodic function which is called each 1 minute and
    notifies user if something is going to happen
    in good way
    or not
    */
    var timeout = 10;
    var notifyBefore = 10; // minutes

    var currentTime = moment();
    var maxTime = moment().add(timeout, 'seconds');

    var allEvents = $("#calendar").fullCalendar('clientEvents');
    for (var eventIndex in allEvents) {
        var event = allEvents[eventIndex];
        if (event.is_notify) {
            var notifyMoment = moment(event.start).subtract(notifyBefore, 'minutes');
            if ((notifyMoment >= currentTime) && (notifyMoment < maxTime)) {
                var message = `Event ${event.title} is coming in ${notifyBefore} minutes`;
                notifyText(message);
            }
        }
    }

    window.setTimeout(isAnythingToNotify, timeout * 1000)
}

function notifyText(text) {
    if (!("Notification" in window)) {
        console.error("This browser does not support desktop notification");
    }

    else if (Notification.permission === "granted") {
        var notification = new Notification(text);
    }

    // Otherwise, we need to ask the user for permission
    else if (Notification.permission !== 'denied') {
        Notification.requestPermission(function (permission) {
          // If the user accepts, let's create a notification
          if (permission === "granted") {
            var notification = new Notification(text);
          }
        });
    }
}
