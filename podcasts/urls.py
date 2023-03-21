from django.urls import path

from .views import HomePageView, see_request, user_info, staff_place, add_messages

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("see_request/", see_request),
    path("user_info/", user_info),
    path("staff_place/", staff_place),
    path("add_messages/", add_messages),
]