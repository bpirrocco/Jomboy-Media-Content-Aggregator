from django.shortcuts import render, HttpResponse, get_list_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView

from .models import Episode, Content

LOGIN_URL = "../accounts/login/"


# TODO: I need to add a favorites page for users that accesses the podcasts_episode_favorite table
#       to show the episodes the user has favorited. Or rather add it as a template I can
#       include using the selector on the dashboard.

class ContentView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/content.html"
    model = Content 
    context_object_name = "content"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = Content.objects.all()
        return context

class EpisodeView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/content_detail.html"
    model = Episode
    context_object_name = "episodes"

    def get_queryset(self):
        qs = super().get_queryset().filter(
            podcast_name_id = self.kwargs["podcast_name_id"]
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = self.get_queryset()
        return context

class DashboardView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/dashboard.html"
    model = Content
    context_object_name = "content"

    def get_queryset(self):
        # self.favorites = get_list_or_404(Content, content_type=self.kwargs['content_type'])
        # self.favorites = self.favorites.filter(favorite=self.request.user)
        if "content_type" in self.kwargs:
            return super().get_queryset().filter(
                favorite=self.request.user).filter(
                    content_type=self.kwargs["content_type"]
                )
        else:
            return super().get_queryset().filter(
                favorite=self.request.user
            )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["episodes"] = Episode.objects.order_by('-pub_date')[:6]
        # if (self.content_type == "PC"):
        #     context["favorites"] = Content.newmanager.filter(favorite=self.request.user).filter(content_type="PC")
        # elif (self.content_type == "YT"):
        #     context["favorites"] = Content.newmanager.filter(favorite=self.request.user).filter(content_type="YT")
        # else:
        #     context["favorites"] = Content.newmanager.filter(favorite=self.request.user)
        context["favorites"] = self.get_queryset()

        return context
