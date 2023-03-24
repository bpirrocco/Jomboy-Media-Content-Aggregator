from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.forms import CustomUserCreationForm

from podcasts.models import Episode

def dashboard(request):
    return render(request, "users/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))

@login_required
def favorite(request, id):
    content = get_object_or_404(Episode, id=id)
    if content.favorite.filter(id=request.user.id).exists():
        content.favorite.remove(request.user)
    else:
        content.favorite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])