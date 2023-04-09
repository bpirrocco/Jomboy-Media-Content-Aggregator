from django.urls import path

from .views import ContentView, DashboardView, EpisodeView

urlpatterns = [
    path("content/", ContentView.as_view(), name = "content"),
    path("dashboard/", DashboardView.as_view(), name = "dashboard"),
    path("dashboard/<str:content_type>/", DashboardView.as_view(), name = "dashboard_filter"),
    path("content/<int:podcast_name_id>/", EpisodeView.as_view(), name = "content_detail"),
]

# I need to alter the dashboard url path to use the new models instead of the content type attributes
# The dashboard template needs to be updated as well to reflect these changes