# encoding=utf-8
from django import forms

from djfp2.calendar.models import CalendarEvent


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = (
            'start_date', 'end_date',
            'title', 'color', 'textcolor',
        )

    def __init__(self, *args, **kwargs):
        try:
            self.owner = kwargs.pop('owner')
        except KeyError:
            self.owner = None
        return super(CalendarEventForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(CalendarEventForm, self).save(*args, **kwargs)
        if self.owner is not None:
            obj.owner = self.owner
        obj.save()
        return obj
