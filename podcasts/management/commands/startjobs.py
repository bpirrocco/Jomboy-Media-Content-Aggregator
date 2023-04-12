# Standard Library
import logging
import os

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

# Functions
from ...common.podcasts.functions import fetch_podcast_data, fetch_podcast_episodes
from ...common.youtube import functions

logger = logging.getLogger(__name__)

feed_dict = {"feed_dict": 
            [{"name": "Talkin' Baseball", "rss_feed": "https://feeds.megaphone.fm/JBM1846488996", "category": "Baseball"},
             {"name": "Rose Rotation", "rss_feed": "https://feeds.megaphone.fm/jbm1555582346", "category": "Baseball"},
             {"name": "Talkin' Giants", "rss_feed": "https://feeds.megaphone.fm/JBM2878672294", "category": "Football"},]}

podcasts = PodcastContent.objects.all()
episode_arg  = {"podcasts": podcasts}

CHANNEL_ID_DICT = {"channel_id_dict":
                  [{"name": "Warehouse Games", "channel_id": "UCIBJINNTKXHp7fkfpJqcpjw", "category": "Sports"}]}

    
def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_podcast_data,
            trigger="interval",
            seconds=30,
            kwargs=feed_dict,
            id="Podcast Data",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Fetch Podcast Data")

        scheduler.add_job(
            fetch_podcast_episodes,
            trigger="interval",
            seconds = 30,
            kwargs=episode_arg,
            id="Podcast Episodes",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Fetch Podcast Episodes")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

