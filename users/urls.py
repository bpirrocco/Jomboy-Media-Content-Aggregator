from django.urls import path, include
from users.views import dashboard, register

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path("register", register, name="register"),
]