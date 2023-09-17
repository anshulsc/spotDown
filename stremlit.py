from dotenv import load_dotenv
from streamlit_card import card
import os
import streamlit as st
from pytube import YouTube
import io
import tempfile
import shutil
from test import songs_demo
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

st.set_page_config(layout="wide")




from spotDown.spotify import get_token, get_playlist_tracks, query_one


def download_song(video_id):
    video = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    stream = video.streams.filter(only_audio=True).first()
    tmp_dir = tempfile.mkdtemp()  # Create a temporary directory
    stream.download(filename=f'{video.title}.mp3',output_path=tmp_dir)  # Download the video to the temporary directory

    downloaded_file_path = f'{tmp_dir}/{video.title}.mp3'
    with open(downloaded_file_path, 'rb') as file:
        file_contents = file.read()
        cards[2].download_button(label="Click to Download MP3",
                                 data=file_contents,
                                 file_name=f"{video.title}.mp3", 
                                 )
    shutil.rmtree(tmp_dir)
    return stream,video


def view_song(video_id,card):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    stream = yt.streams.get_highest_resolution()
    tmp_dir = tempfile.mkdtemp()  # Create a temporary directory
    stream.download(filename=f"{yt.title}.mp4",output_path=tmp_dir)  # Download the video to the temporary directory
    card.video(f"{tmp_dir}/{yt.title}.mp4")

  
    shutil.rmtree(tmp_dir)


token = get_token(client_id, client_secret)

playlist_links = st.text_input('Spotify Playlist Link', 'https://open.spotify.com/playlist/3Is0HkDrq54YAiYHNHElbg?si=b3c47e8eb2b04214')
if playlist_links == "https://open.spotify.com/playlist/3Is0HkDrq54YAiYHNHElbg?si=b3c47e8eb2b04214":
    songs = songs_demo
else:
    songs = get_playlist_tracks(playlist_links ,token)
    songs = query_one(songs)

print(songs)
st.write(songs)


with st.container():
    for key in songs.keys(): 
        st.write('<div class="song-details-container">', unsafe_allow_html=True)

        image_details = f"""
        <div class="image-card">
            <img src="{songs[key]['url']}" alt="{key}" width="200">
        </div>
    """
        cards = st.columns([0.2,0.6,0.1])

        cards[0].write(image_details,unsafe_allow_html=True)
        song_details = f"""
    <div class="song-card">
        <h2>{key}</h2>
        <p><em>{songs[key]['Artist'][0]}</em></p>
        <p> Youtube Link: <a href = {songs[key]['yt_url']}>{songs[key]['yt_url']}</a></p>
    </div>
    """
        cards[1].write(song_details, unsafe_allow_html=True)
        with cards[2]:
            placeholder =  st.selectbox(" ",
    ('','MP3', 'Video'), placeholder='Get...',key=f'{key}')

            if placeholder == "MP3":
                with st.spinner("Fetching ..."):
                    stream, video =  download_song(songs[key]["video_id"])
            if placeholder == 'Video':
                view_song(songs[key]["video_id"],cards[1])
        st.write('</div>', unsafe_allow_html=True)






st.markdown("""
<style>
.song-details-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.song-card {
    background-color: #f5f5f5;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.song-card:hover {
    background-color: #f5f5f3;
    transform: scale(1.05);
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.image-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
    transition: transform 0.3s ease;
}


.image-card img {
    max-width: 100%;
    border-radius: 10px;
    transition: transform 0.3s ease;
}

.image-card:hover img {
    transform: scale(1.1);
}

.video-card {
    background-color: #f5f5f5;
    padding: 20px;
    margin: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
}

video {
    width: 100%;
    border-radius: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    outline: none;
}

video::after {
    content: "\\25B6";
    font-size: 3rem;
    color: #fff;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    cursor: pointer;
}

/* Hover effect for the play button */
video:hover::after {
    transform: translate(-50%, -50%) scale(1.2);
}

h2 {
    font-size: 24px;
    margin: 0;
    color: #000;
}

em {
    color: #888;
}

p {
    margin: 5px 0;
    color: #000;
}

/* Dark mode styles */
.dark-mode .song-card,
.dark-mode .image-card,
.dark-mode .video-card {
    background-color: #333;
    box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
    color: #fff;
}

/* Media queries for responsiveness */
@media (max-width: 768px) {
    .song-details-container {
        flex-direction: column;
    }

    .song-card,
    .image-card,
    .video-card {
        width: 100%;
    }

    .image-card {
        text-align: center;
    }

    video::after {
        font-size: 2rem;
    }
}

</style>
""", unsafe_allow_html=True)