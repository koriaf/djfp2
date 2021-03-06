from django.conf.urls import url

from djfp2.calendar.views import (
    EventsGetView, EventsCreateView, EventsUpdateView, EventsRemoveView,
)

urlpatterns = [
    url(r'^events/get/$', EventsGetView.as_view(), name='events_get'),
    url(r'^events/create/$', EventsCreateView.as_view(), name='events_create'),
    url(r'^events/update/$', EventsUpdateView.as_view(), name='events_update'),
    url(r'^events/remove/$', EventsRemoveView.as_view(), name='events_remove'),
]
