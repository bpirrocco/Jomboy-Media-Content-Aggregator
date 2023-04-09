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
        feed_string = item.get("rss_feed")
        feed_object = feedparser.parse(feed_string)
        category = item.get("category")
        save_new_podcast(feed_object, feed_string, category)

def save_new_podcast(feed_object, feed_string, category):
    """Saves new content to the database.


    Checks the content name against the content currently stored in the

    database. If not found, then a new `Content` is added to the database.


    Args:

        feed: requires a feedparser object

    """
    name = feed_object.channel.title

    if not PodcastContent.objects.filter(name=name).exists():
        content = PodcastContent(
        name = name,
        description = feed_object.channel.description,
        image = feed_object.channel.image["href"],
        categories = category,
        link = feed_object.channel.link,
        rss = feed_string
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
        feed_object = feedparser.parse(rss)
        save_new_episodes(feed_object, podcast_title)

def save_new_episodes(feed_object, podcast_title):
    """Saves new episodes to the database.


    Checks the episode GUID against the episodes currently stored in the

    database. If not found, then a new `Episode` is added to the database.


    Args:

        feed: requires a feedparser object

    """
    # podcast_title = feed.channel.title
    podcast_image = feed_object.channel.image["href"]

    for item in feed_object.entries:
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