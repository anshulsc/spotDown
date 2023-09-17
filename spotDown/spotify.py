from dotenv import load_dotenv
import os 
import requests
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Getting Access token 
def get_token(client_id,client_secret) -> str:

        url = 'https://accounts.spotify.com/api/token'
        auth = client_id + ':' + client_secret
        auth =  auth.encode('utf-8')
        auth_code = str(base64.b64encode(auth), 'utf-8')

        headers = {
            'Authorization': 'Basic ' + auth_code,
            'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials'}

        res = requests.post(url, headers=headers, data=data)
        return json.loads(res.content)['access_token']

def gen_token() -> str:
    return get_token(client_id,client_secret)


# lambda function to get playlist id 
get_playlist_id = lambda x : x.split('/')[-1].split('?')[0]

def get_playlist(playlist: str, token):
    playlist_id = get_playlist_id(playlist)

    endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    access_header = {
        'Authorization': 'Bearer ' + token
        }
    res = requests.get(endpoint, headers=access_header)
    total = json.loads(res.content)['tracks']['total']
    item_length = len(json.loads(res.content)['tracks']['items'])
    return total, item_length



def get_playlist_tracks(playlist: str, token):

    playlist_id = get_playlist_id(playlist)
    total, item_length = get_playlist(playlist, token)
    print(f"Total: {total}, item_length: {item_length}")
    songs = {}

    limit = 100
    for i in range(0, total, limit):
        endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}&offset={i}'
        access_header = {
                'Authorization': 'Bearer ' + token
                }
        res = requests.get(endpoint, headers=access_header)
            
        playlist = json.loads(res.content)
        songs.update({ playlist['items'][i]['track']['name']: {'Artist' :  [playlist['items'][i]['track']['artists'][0]['name']  ]
                                                               ,'url' : playlist['items'][i]['track']['album']['images'][0]['url']}
                                                               for i in range(len(playlist['items']))})
    return songs


# token = get_token(client_id,client_secret)
playlist_link = 'https://open.spotify.com/playlist/6pOAWULl15h5nP3syN7O3w?si=63bb1fec97114cda'

def query(songs):
    queries = []
    for song, artist in songs.items():
        query = f'{song} {artist} official music video'.replace(' ', '%20')
        youtube_api = 'AIzaSyAIa59pWRao9Z33pdFfenK0rltA5Y3ZgoA'
        youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={youtube_api}&type=video&videoSyndicated=true&type=video'
        try:
            res = requests.get(youtube_url)
            video_id = json.loads(res.content)['items'][0]['id']['videoId']
            url = f'https://www.youtube.com/watch?v={video_id}'
            queries.append({'song':song,'video_id': video_id, 'url': url})
        except:
            print(f'Error {json.loads(res.content)}')
            break
    return queries


def query_one(songs):
    for key in songs.keys():
        print()
        query = f'{key} - {songs[key]["Artist"][0]} official song'.replace(' ', '%20')
        youtube_api = 'AIzaSyAIa59pWRao9Z33pdFfenK0rltA5Y3ZgoA'
        youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={youtube_api}&type=video&videoSyndicated=true&type=video'
        try:
            res = requests.get(youtube_url)
            video_id = json.loads(res.content)['items'][0]['id']['videoId']
            songs[key]['video_id'] = video_id
            url = f'https://www.youtube.com/watch?v={video_id}'
            songs[key]['yt_url'] = url
    
        except:
            print(f'Error {json.loads(res.content)}')
            break
    return songs


