from dotenv import load_dotenv
from streamlit_card import card
import streamlit as st
import numpy as np
import streamlit as st
import subprocess
from pytube import YouTube

# image = st.camera_input("Show QR code")

# if image is not None:
#     bytes_data = image.getvalue()
#     cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

#     detector = cv2.QRCodeDetector()

#     data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

#     st.write("Here!")
#     st.write(data)

# from streamlit_qrcode_scanner import qrcode_scanner

# qr_code = qrcode_scanner(key='qrcode_scanner')

# if qr_code:
#     st.write(qr_code)

import os
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


from spotDown.spotify import get_token, get_playlist_tracks, query_one

def download_video(video_id):
    # try:
    #     subprocess.run(['youtube-dl', f'https://www.youtube.com/watch?v={video_id}', '--extract-audio', '-x', '--audio-format', 'mp3', '--audio-quality', '0', '-o',f"downloads/%(title)s.%(ext)s"],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,)
    # except Exception as e:
    #         st.error(f"An error occurred: {str(e)}")
    video = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    stream = video.streams.filter(only_audio=True).first()
    return stream , video



token = get_token(client_id, client_secret)

playlist_links = st.text_input('Spotify Playlist Link', 'Life of Brian')

songs = get_playlist_tracks(playlist_links ,token)


songs = query_one(songs)

st.write(songs)


with st.container():
    for key in songs.keys(): 
        cards = st.columns(3)

        cards[0].image(
            f"{songs[key]['url']}",
            width=100, # Manually Adjust the width of the image as per requirement
        )
        cards[1].write(key)
     
        if cards[2].button('Download',key=f'{key}'):
            stream, video =  download_video(songs[key]["video_id"])
            stream.download(filename=f"{video.title}.mp3")
        st.success(f'Download completed for video with ID: {songs[key]["video_id"]}')


    #     hasClicked = card(
    # title=f"{key}",
    # text="Some description",
    # image=f"{songs[key]['url']}",
    # styles={
    #         "card": {
    #             "width": "250px",
    #             "height": "250px",
    #             "border-radius": "60px",
    #             "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
        
    #         }
    # }
    # )