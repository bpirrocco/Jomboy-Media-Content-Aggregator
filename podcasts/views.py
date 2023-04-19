from django.shortcuts import render, HttpResponse, get_list_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView

from .models import Episode, Content, YoutubeContent, PodcastContent

from .common.youtube.functions import create_video_list

LOGIN_URL = "../accounts/login/"

class PodcastView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/content.html"
    model = PodcastContent 
    context_object_name = "content"

    def get_queryset(self):
        return super().get_queryset().filter(
            favorite = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = PodcastContent.objects.all()
        context["favorites"] = self.get_queryset()
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
        context["jumbotron"] = self.get_queryset()[0].image
        return context

class DashboardView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/dashboard.html"
    model = Content
    context_object_name = "content"

    # I need to change this view to use the new multitable models I created
    # I probably don't need to use the get_queryset method anymore, just a simple
    # if statement that grabs all Podcast/Youtube content objects

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

class YoutubeContentView(LoginRequiredMixin, ListView):
    login = LOGIN_URL

    template_name = "dashboard/youtube_content.html"
    model = YoutubeContent
    context_object_name = "channel"


    def get_queryset(self):
        qs = super().get_queryset().filter(
            name = self.kwargs["name"]
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel"] = self.get_queryset
        context["jumbotron"] = self.get_queryset()[0].image
        context["video_list"] = create_video_list(self.get_queryset()[0].upload_id)

        return context

def TestView(request):
    video = "HVsySz-h9r4"
    return render(request, "dashboard/iframe_player.html", {"video": video})