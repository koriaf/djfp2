# -*- coding: utf-8 -*-
from django.contrib import admin

from djfp2.calendar.models import CalendarEvent


class CalendarEventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'owner', 'start_date', 'end_date', 'textcolor', 'color', 'is_notify'
    )

admin.site.register(CalendarEvent, CalendarEventAdmin)
