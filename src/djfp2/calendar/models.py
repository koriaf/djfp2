# encoding=utf-8
from django.db import models
from django.conf import settings


class CalendarEvent(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_date = models.DateTimeField(u"Local start datetime")
    end_date = models.DateTimeField(u"Local end datetime")
    title = models.CharField(max_length=1000)
    color = models.CharField(max_length=40, blank=True, default="#6aa4c1")
    textcolor = models.CharField(max_length=40, blank=True, default="black")

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return u"{} {}: {}".format(self.owner, self.title, self.start_date)

    def get_as_fullcalendar_event(self):
        result = {
            'id': self.id,
            'start': self.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': self.end_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'title': self.title,
            'backgroundColor': self.color,
            'textColor': self.textcolor,
        }
        return result
