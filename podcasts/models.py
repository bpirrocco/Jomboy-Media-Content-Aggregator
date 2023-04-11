from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Content(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() 


    # PODCAST = "PC"
    # YOUTUBE = "YT"
    # CONTENT_TYPE_CHOICES = [
    #     (PODCAST, "Podcast"),
    #     (YOUTUBE, "Youtube")
    # ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    categories = models.TextField()
    link = models.URLField()
    # content_type = models.CharField(max_length=7, choices=CONTENT_TYPE_CHOICES)
    favorite = models.ManyToManyField(User, related_name="content_favorite", default=None, blank=True)
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def __str__(self) -> str:
        return f"{self.name}"

class PodcastContent(Content):

    rss = models.URLField()

class YoutubeContent(Content):

    channel_id = models.CharField(max_length=100)
    upload_id = models.CharField(max_length=100)

class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(PodcastContent, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name="episode_favorite", default=None, blank=True)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"

# DONE: I need to make a multitable model for the Podcast Episodes and the Youtube Videos
#       This is not necessary, as I'm pulling the youtube videos in using the API, never storing them in the db

# TODO: I need to change the content detail view to use the new multitable views
# TODO: Pull in a few Jomboy Youtube channels
# TODO: Fill out all dead links
# TODO: Style all users templates
# TODO: Look into migrating this to a Postgres Database
# That should be enough to call this app done! 