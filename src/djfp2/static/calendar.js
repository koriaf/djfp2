var timelineInterval;

$(document).ready(function() {
    $('#calendar').fullCalendar({
        // http://fullcalendar.io/docs/
        defaultView: 'agendaWeek',
        editable: true,
        allDaySlot: false,
        axisFormat: 'HH:mm',
        timeFormat: 'HH:mm',
        minTime: '07:00:00',
        timezone: 'local',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        snapDuration: '00:10:00',
        firstDay: 1,
        eventTextColor: '#000000',
        eventColor: '#6aa4c1',
        events: '/calendar/events/get/',
        eventClick: PlannerLib.calendar.eventClick,
        eventResize: PlannerLib.calendar.eventChange,
        eventDrop: PlannerLib.calendar.eventChange,
        dayClick: PlannerLib.calendar.dayClick,
        viewRender: function(view) {              
            if(typeof(timelineInterval) != 'undefined'){
              window.clearInterval(timelineInterval); 
            }
            timelineInterval = window.setInterval(PlannerLib.calendar.setTimeline, 30000);
            try {
              PlannerLib.calendar.setTimeline();
            } catch(err) {}
        },
    });

    // this red line, following current moment of time
    PlannerLib.calendar.setTimeline();

    // add csrf token to every ajax request
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
        } 
    });

    // hide popup on ESC key press or close button
    $(document).keyup(function(e) {
        if (e.keyCode == 27) { $('#popup').hide(); }
    });
    $("#popup_close_button").click(function() {
        $('#popup').hide();
    });

    // and some popup functionality
    $("#popup_save_button").click(PlannerLib.calendar.popup.pressSaveButton);
    $("#popup").keyup(function(e) {
        if (e.keyCode == 13) {
            $("#popup_save_button").click();
        }
    });

    $("#popup_delete_button").click(PlannerLib.calendar.popup.pressDeleteButton);
    $("#popup #colors_choicer .color_block").click(PlannerLib.calendar.eventColorChange);

    $(window).resize(PlannerLib.calendar.setTimeline);
});
