from django.urls import path

from .views import PodcastView, DashboardView, EpisodeView

urlpatterns = [
    path("podcasts/", PodcastView.as_view(), name = "podcasts"),
    path("dashboard/", DashboardView.as_view(), name = "dashboard"),
    path("dashboard/<str:content_type>/", DashboardView.as_view(), name = "dashboard_filter"),
    path("content/<int:podcast_name_id>/", EpisodeView.as_view(), name = "content_detail"),
]