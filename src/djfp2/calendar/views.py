# encoding: utf-8
from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "calendar/home.html"
