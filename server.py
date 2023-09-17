from fastapi import FastAPI
# from fastapi_cache import FastAPICache, caches
# from fastapi_cache.backends.filesystem import FileSystemCache
import spotDown.spotify as spotify

app = FastAPI()



@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/spotify/playlist/")
def get_playlist_tracks(playlist: str):
    token = spotify.gen_token()
    return spotify.get_playlist_tracks(playlist, token)

@app.get("/spotify/playlist/get_tracks")
def get_playlist_tracks(playlist: str):
    token = spotify.gen_token()
    songs = spotify.get_playlist_tracks(playlist, token)
    return spotify.query(songs)