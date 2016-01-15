# encoding: utf-8
from braces.views import LoginRequiredMixin, JSONResponseMixin
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404

from djfp2.calendar.forms import CalendarEventForm
from djfp2.calendar.models import CalendarEvent


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "calendar/home.html"


class EventsGetView(LoginRequiredMixin, JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        events = CalendarEvent.objects.filter(
            owner=request.user,
            start_date__gte=request.GET.get('start'),
            end_date__lte=request.GET.get('end'),
        )
        rows = [event.get_as_fullcalendar_event() for event in events]
        return self.render_json_response(rows)


class EventsUpdateView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(
            CalendarEvent,
            owner=request.user,
            id=request.POST.get('event_id', 0)
        )
        event_form = CalendarEventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
        else:
            self.render_json_response(event_form.errors)
        return self.render_json_response({
            'result': 'success'
        })


class EventsRemoveView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        event = get_object_or_404(
            CalendarEvent,
            owner=request.user,
            id=request.POST.get('event_id', 0)
        )
        event.delete()
        return self.render_json_response({
            'result': 'success'
        })


class EventsCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        event_form = CalendarEventForm(request.POST, owner=request.user)
        if event_form.is_valid():
            event = event_form.save()
            data = event.get_as_fullcalendar_event()
            data['event_to_replace'] = request.POST.get('event_to_replace')
            data['result'] = 'success'
            return self.render_json_response(data)
        else:
            return self.render_json_response({
                'result': 'error',
                'message': event_form.errors
            })
