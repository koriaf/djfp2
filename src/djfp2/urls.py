# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

from djfp2.calendar.views import HomeView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^calendar/', include('djfp2.calendar.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}),

    url(r'^admin/', include(admin.site.urls)),
)
