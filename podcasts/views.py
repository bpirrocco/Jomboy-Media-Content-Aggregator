from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from .models import Episode

LOGIN_URL = "../accounts/login/"


# TODO: I need to add a favorites page for users that accesses the podcasts_episode_favorite table
#       to show the episodes the user has favorited. Or rather add it as a template I can
#       include using the selector on the dashboard.

class PodcastView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL
    # redirect_field_name = "redirect_to"

    template_name = "dashboard/podcasts.html"
    model = Episode 
    context_object_name = "episodes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Episode.objects.filter().order_by("-pub_date")[:10]
        return context

class DashboardView(LoginRequiredMixin, ListView):
    login_url = LOGIN_URL

    template_name = "dashboard/dashboard.html"
    model = Episode
    context_object_name = "episodes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Episode.objects.order_by('-pub_date')[:6]
        return context

def see_request(request):
    text = f"""
        Some attributes of the HttpRequest object:

        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
    """

    return HttpResponse(text, content_type="text/plain")


def user_info(request):
    text = f"""
        Selected HttpRequest.user attributes:

        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    return HttpResponse(text, content_type="text/plain")

@user_passes_test(lambda user: user.is_staff)
def staff_place(request):
    return HttpResponse("Employees must wash hands", content_type="text/plain")

@login_required
def add_messages(request):
    username = request.user.username
    messages.add_message(request, messages.INFO, f"Hello {username}")
    messages.add_message(request, messages.WARNING, "DANGER WILL ROBINSON")

    return HttpResponse("Messages added", content_type="text/plain")