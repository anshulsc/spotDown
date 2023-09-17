from dotenv import load_dotenv
import os 
import requests
import base64
import json
import argparse
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


from spotDown.spotify import get_token, get_playlist_tracks, query
from youtube import download_yt



token = get_token(client_id, client_secret)

playlist_link = 'https://open.spotify.com/playlist/2locirv8HzqrvEti5XonTF?si=073701edb83a4c97'

def get_songs(playlist_link):
    songs = query(get_playlist_tracks(playlist_link, token))
    print(songs)
    download_yt(songs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("plink", help="Spotify Playist link")
    args = parser.parse_args()
    print(args.plink)
    get_songs(args.plink)
