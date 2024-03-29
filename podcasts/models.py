from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Content(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() 


    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    image = models.URLField()
    categories = models.TextField()
    favorite = models.ManyToManyField(User, related_name="content_favorite", default=None, blank=True)
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def __str__(self) -> str:
        return f"{self.name}"

class PodcastContent(Content):

    rss = models.URLField()
    link = models.URLField()

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

# TODO: Pull in a few Jomboy Youtube channels
# TODO: Fill out all dead links
# TODO: Style all users templates
# TODO: Look into migrating this to a Postgres Database
# That should be enough to call this app done! 