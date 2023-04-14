from django.urls import path

from .views import ContentView, DashboardView, EpisodeView, YoutubeContentView

urlpatterns = [
    path("content/", ContentView.as_view(), name = "content"),
    path("dashboard/", DashboardView.as_view(), name = "dashboard"),
    path("dashboard/<str:content_type>/", DashboardView.as_view(), name = "dashboard_filter"),
    path("content/<int:podcast_name_id>/", EpisodeView.as_view(), name = "content_detail"),
    path("content/<str:name>/", YoutubeContentView.as_view(), name = "youtube_content"),
]