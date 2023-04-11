import os
import json

import pandas as pd

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from django.conf import settings

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

feed_dict = [{"rss_feed": "rss", "genre": "baseball"}, {"rss_feed": "rss", "genre": "baseball"}, {"rss_feed": "rss", "genre": "football"}]

def get_video_ids(response):
    data = []
    for i in range(len(response['items'])):
        url = response['items'][i]["snippet"]["resourceId"]["videoId"]
        data.append(url)
    return data


# I don't think this create urls will be necessary. It would be cool to embed the youtube iframe player api
# and programmatically add the videoId needed to play the video instead
# Maybe something where when the user selects a video, a youtube player appears loaded with the videoId added

# Side note: it would be cool to embed a podcast player of some sort as well so a user can listen to the podcasts
# in app as well

def create_video_urls(data):
    url_list = []
    for item in data:
        url_list.append(("https://www.youtube.com/watch?v=" + item))
    return url_list

def main(playlist_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE, scopes)
    # credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=settings.YOUTUBE_API_KEY)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId=playlist_id
    )
    response = request.execute()

    data = get_video_ids(response)

    data = create_video_urls(data)

    print(data)

# if __name__ == "__main__":
    # playlist_id = "UUl9E4Zxa8CVr2LBLD0_TaNg"
    # main()
    for item in feed_dict:
        print(item.get("rss_feed"))
        print(item.get("genre"))