from django.urls import path, include
from users.views import dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("", dashboard, name="dashboard"),
]