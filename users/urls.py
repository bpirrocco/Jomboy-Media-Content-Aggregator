from django.urls import path, include
from users.views import dashboard, register, favorite

app_name= "users"

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('social/', include('social_django.urls', namespace='social')),
    path("register", register, name="register"),
    path("favorite/<int:id>/", favorite, name="favorite_add")
]