import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os
import youtube_dl 
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
# class Create_playlist():
#     def __init__(self):
#         self.user_id = spotify_user_id
spotify_token = 'BQB_Tz3WHtLS3VUOIhU6Do1AP_tDfR20guwyVK0E5QxPcS9y_ydTt_XffBpD43qpm_u2Tk9VkOHjWBjlL8vbjK3JmBnA4g7v0zEpVIjGeklAfejDGDCgGyXSp4jq4vuBAWYgWAsDrPlKY857AQi2VdW8Tzg7Ki_PjIOgvKi_7G6DiMMBTCe395mUow'
spotify_user_id ='nghhaidang-usbfie3'
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

#Step 1: log into youtube 
def get_youtube_client():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = "PLxt-QTFbOqCnPtgt1fq5xBlrqIDP_9uSy"
    )
    response = request.execute()
    return response



#step 2: get playlist
def get_songs(dic):
    url = "https://www.youtube.com/watch?v="
    info = []
    song = ""
    for i in range(len(dic["items"])):
        video_url = url+str(dic["items"][i]["snippet"]["resourceId"]['videoId'])
        details = youtube_dl.YoutubeDL(
            {}).extract_info(video_url, download=False)
        if 'track' not in details:
            continue
        if 'artist'not in details:
            continue
        track = details['track']
        artist =  details['artist']
        info.append((track,artist))
    return info 

# def get_song():
#     for item in response["items"]:
#         info = []
#         video_title = item["snippet"]["title"]
#         youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])
#         details = youtube_dl.YoutubeDL(
#             {}).extract_info(youtube_url, download=False)
#         track = details['track']
#         artist =  details['artist']
#         info.append((track,artist))

#step 3: create playlist
def create_spotify_playlist():
    request_body = json.dumps({
        "name": "Mate's playlist",
        "description": "something",
        "public": True}
    )
    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
    response = requests.post(
        query,
        data = request_body, 
        headers = {"Content-Type": "application/json", 
        "Authorization": "Bearer {}".format("spotify_token")                                
        })
    response = response.json()
    return response

#step 4: Find song
def get_spotify_uri(track, artist):
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track".format(track, artist)

    response = requests.post(
        query, 
        headers = {"Content-Type": "application/json", 
        "Authorization": "Bearer {}".format("spotify_token")                                
        })
    # if int(response.status_code) == 200 :
    #     songs = response["track"]["artist"]
    #     url = songs[0]["uri"]
    #     return url
    
#step 5: add song
def add_song_to_playlist(playlist_id, urls):
    request_data = json.dump(urls)
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    response = requests.post(
        query, 
        data = request_data, 
        headers = {"Content-Type": "application/json", 
        "Authorization": "Bearer {}".format("spotify_token")}      
    )
    return "songs added"

response = get_youtube_client()
play_id = create_spotify_playlist()
song_info = get_songs(response)

urls = []
for i in range(len(response['items'])):
    # if not get_spotify_uri(song_info[i][0], song_info[i][0]) :
    #     continue
    # print(get_spotify_uri(song_info[i][0], song_info[i][0]))
    # print(song_info[i][0])
    # print(song_info[i][0])
    # urls.append(get_spotify_uri(song_info[i][0], song_info[i][0]))
    urls.append(get_spotify_uri('Wrecked', 'Wrecked'))
add_song_to_playlist(play_id, urls)