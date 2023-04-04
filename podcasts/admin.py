from django.contrib import admin

from .models import Episode, Content

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", "title", "pub_date")

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("name", "content_type", "categories")
