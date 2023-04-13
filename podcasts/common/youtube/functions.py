import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from django.conf import settings

from podcasts.models import YoutubeContent

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


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
    youtube_content = YoutubeContent(
        name = response_item["snippet"]["title"],
        description = response_item["snippet"]["description"],
        image = response_item["snippet"]["thumbnails"]["high"]["url"],
        categories = category,
        channel_id = response_item["id"],
        upload_id = response_item["contentDetails"]["relatedPlaylists"]["uploads"],
    )
    youtube_content.save()


# ***************
# Views Functions
# ***************


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
        id=upload_id,
    )
    response = request.execute()

    return response