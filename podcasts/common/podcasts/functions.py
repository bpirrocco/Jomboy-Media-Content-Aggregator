# Standard Library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode, Content, PodcastContent, YoutubeContent


# *******************************
# Podcast Data Fetching Functions
# *******************************


def fetch_podcast_data(feed_dict):
    """Fetches data to create PodcastContent objects.
    
        Args:
            
            feed_dict: a dictionary of RSS Feeds mapped to their genre
            
    """
    for item in feed_dict:
        feed = item.get("rss_feed")
        category = item.get("category")
        save_new_podcast(feed, category)

def save_new_podcast(feed, category):
    """Saves new content to the database.


    Checks the content name against the content currently stored in the

    database. If not found, then a new `Content` is added to the database.


    Args:

        feed: requires a feedparser object

    """
    name = feed.channel.title

    if not Content.objects.filter(name=name).exists():
        content = Content(
        name = name,
        description = feed.channel.description,
        image = feed.channel.image["href"],
        categories = category,
        link = feed.channel.link,
        # content_type = "PC"
        )
        content.save()


# *****************************
# Podcast Episode Data Fetching
# *****************************


def fetch_podcast_episodes(podcasts):
    """Fetches episode information from a list of Podcast objects.
    
        Args: 
            
            podcasts: list of Podcast objects.
    
    """
    for podcast in podcasts:
        rss = podcast.rss
        podcast_title = podcast.id
        _feed = feedparser.parse(rss)
        save_new_episodes(_feed, podcast_title)

def save_new_episodes(feed, podcast_title):
    """Saves new episodes to the database.


    Checks the episode GUID against the episodes currently stored in the

    database. If not found, then a new `Episode` is added to the database.


    Args:

        feed: requires a feedparser object

    """
    # podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            i = 0
            episode = Episode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link = item.enclosures[i]["href"],
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()
            i+=1