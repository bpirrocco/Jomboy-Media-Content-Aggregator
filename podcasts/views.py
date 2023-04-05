from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import Episode, Content

LOGIN_URL = "../accounts/login/"


# TODO: I need to add a favorites page for users that accesses the podcasts_episode_favorite table
#       to show the episodes the user has favorited. Or rather add it as a template I can
#       include using the selector on the dashboard.

class PodcastView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/podcasts.html"
    model = Content 
    context_object_name = "content"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = Content.objects.filter().order_by("name")[:10]
        return context

class DashboardView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/dashboard.html"
    model = Episode
    context_object_name = "episodes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Episode.objects.order_by('-pub_date')[:6]
        # context["favorites"] = Episode.objects.filter(favorite=self.request.user)
        context["favorites"] = Content.newmanager.filter(favorite=self.request.user)
        return context
