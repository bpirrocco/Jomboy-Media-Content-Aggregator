import os
import logging

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from django.conf import settings

from podcasts.models import YoutubeContent

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

logger = logging.getLogger(__name__)


# *******************
# StartJobs Functions
# *******************


def fetch_youtube_channels(channel_id_dict):
    """Fetches data to create YoutubeContent objects.
    
        Args:
            
            channel_id_dict: a dictionary of channel_id's mapped to their genre
           
    """

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME, API_VERSION, developerKey=settings.YOUTUBE_API_KEY,
    cache_discovery=False)

    channel_id_list = []
    for item in channel_id_dict:
        channel_id_list.append(item.get("channel_id"))
        channel_id_list = ','.join(channel_id_list)

    category_list = []
    for item in channel_id_dict:
        category_list.append(item.get("category"))
        category_list.reverse()

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        maxResults=25,
        id=channel_id_list,
    )
    response = request.execute()

    for i in range(len(response['items'])):
        save_new_channel(response["items"][i], category_list[i])

def save_new_channel(response_item, category):
    """Saves new YoutubeContent to the database.


    Checks the channel_id against the content currently stored in the

    database. If not found, then a new `YoutubeContent` is added to the database.


    Args:

        response_item: requires a response item from the youtube api

        category: a category for the YoutubeContent database entry

    """
    channel_id = response_item["id"]

    if not YoutubeContent.objects.filter(channel_id=channel_id).exists():
        youtube_content = YoutubeContent(
            name = response_item["snippet"]["title"],
            description = response_item["snippet"]["description"],
            image = response_item["snippet"]["thumbnails"]["high"]["url"],
            categories = category,
            channel_id = channel_id,
            upload_id = response_item["contentDetails"]["relatedPlaylists"]["uploads"],
        )
        youtube_content.save()


# ***************
# Views Functions
# ***************


class YoutubeVideo:
    def __init__(self, name, description, pub_date, thumbnail, video_id, channel_id, **kwargs):
        self.name = name
        self.description = description
        self.pub_date = pub_date
        self.thumbnail = thumbnail
        self.video_id = video_id
        self.channel_id = channel_id

def fetch_upload_playlist(upload_id):
    """Fetches uploads playlist data from Youtube data API.
    
    Used by YoutubeContentView
    
    Args:
    
        upload_id: the upload id for a given youtube channel
        
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
    API_SERVICE_NAME, API_VERSION, developerKey=settings.YOUTUBE_API_KEY,
    cache_discovery=False)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId=upload_id,
    )
    response = request.execute()

    return response

def create_youtube_video(video):
    """Creates a YoutubeVideo object.
    
    Args: 
    
        video: a single video item returned from the Youtube API
        
    """
    video_object = YoutubeVideo(
        name = video["snippet"]["title"],
        description = video["snippet"]["description"],
        pub_date = video["snippet"]["publishedAt"],
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"],
        video_id = video["contentDetails"]["videoId"],
        channel_id = video["snippet"]["channelId"],
    )

    return video_object

def create_video_list(upload_id):
    """Fetches and formats data for YoutubeContentView.
    
    Args: 
    
        upload_id: the upload id for a given youtube channel
        
    """
    video_list = []
    response = fetch_upload_playlist(upload_id)

    for item in response['items']:
        video = create_youtube_video(item)
        video_list.append(video)
    
    return video_list