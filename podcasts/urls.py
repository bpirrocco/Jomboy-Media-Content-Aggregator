from django.urls import path

from .views import PodcastView, DashboardView

urlpatterns = [
    path("podcasts/", PodcastView.as_view(), name = "podcasts"),
    path("dashboard/", DashboardView.as_view(), name = "dashboard"),
]