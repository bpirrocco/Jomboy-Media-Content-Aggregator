from django.contrib import admin

from .models import Episode, Content, PodcastContent, YoutubeContent

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", "title", "pub_date")

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("name", "categories")

@admin.register(PodcastContent)
class PodcastContentAdmin(admin.ModelAdmin):
    list_display = ("name", "categories")

@admin.register(YoutubeContent)
class YoutubeContentAdmin(admin.ModelAdmin):
    list_display = ("name", "categories")
