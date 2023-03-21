from django.urls import path

from .views import HomePageView, DashboardView

urlpatterns = [
    path("", HomePageView.as_view(), name = "homepage"),
    path("dashboard/", DashboardView.as_view(), name = "dashboard"),
]