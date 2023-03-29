from django.db import models
from django.contrib.auth.models import User

class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.CharField(max_length=100)
    favorite = models.ManyToManyField(User, related_name="favorite", default=None, blank=True)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"

class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    categories = models.TextField()
    
