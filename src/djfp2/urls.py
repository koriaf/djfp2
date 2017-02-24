from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as login_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from djfp2.calendar.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^calendar/', include('djfp2.calendar.urls')),

    url(r'^accounts/login/$', login_views.login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', login_views.login, {'template_name': 'login.html'}),

    url(r'^admin/', include(admin.site.urls)),
]


# it's better when nginx doesn't let any /static/ requests to reach django app, but
# fallback solution for simple installations also useful
urlpatterns += staticfiles_urlpatterns()
