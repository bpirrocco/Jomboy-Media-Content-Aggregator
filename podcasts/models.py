from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Content(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() 


    PODCAST = "PC"
    YOUTUBE = "YT"
    CONTENT_TYPE_CHOICES = [
        (PODCAST, "Podcast"),
        (YOUTUBE, "Youtube")
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    categories = models.TextField()
    link = models.URLField()
    content_type = models.CharField(max_length=7, choices=CONTENT_TYPE_CHOICES)
    favorite = models.ManyToManyField(User, related_name="content_favorite", default=None, blank=True)
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def __str__(self) -> str:
        return f"{self.content_type}: {self.name}"

class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(Content, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name="episode_favorite", default=None, blank=True)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"