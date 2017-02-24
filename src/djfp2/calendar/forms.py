import dateutil.parser
from django import forms

from djfp2.calendar.models import CalendarEvent


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = (
            'start_date', 'end_date',
            'title', 'color', 'textcolor',
            'is_notify',
        )

    def __init__(self, data, *args, **kwargs):
        try:
            self.owner = kwargs.pop('owner')
        except KeyError:
            self.owner = None
        rasterized_data = {}
        for field_name in self.Meta.fields:
            value = data.get(field_name)
            if value is not None:
                if isinstance(value, list):
                    rasterized_data[field_name] = value[0]
                else:
                    rasterized_data[field_name] = value
        rasterized_data['start_date'] = dateutil.parser.parse(rasterized_data['start_date'])
        rasterized_data['end_date'] = dateutil.parser.parse(rasterized_data['end_date'])
        # print("User sent start_date %s which was interpreted as %s" % (data['start_date'], rasterized_data['start_date']))
        return super(CalendarEventForm, self).__init__(rasterized_data, *args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(CalendarEventForm, self).save(*args, **kwargs)
        if self.owner is not None:
            obj.owner = self.owner
        obj.save()
        return obj
