import streamlit as st
from pytube import Playlist, YouTube
import os
st.set_page_config(page_title="Youtube Playlist Downloader")


# Style
st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-color: green;
        }

        /* Style for the empty part of the progress bar */
        .stProgress > div > div > div {
            background-color: white;
        }
    </style>""",
    unsafe_allow_html=True,
)

def download_videos(playlist_url):
    pl = Playlist(playlist_url)
    total_videos = len(pl.video_urls)
    progress_bar = st.progress(0)
    i = 0
    for video_url in pl.video_urls:
        i += 1
        try:
            yt = YouTube(video_url)
            author = yt.author.replace("/", "_").replace(":", "_")  # Sanitize author name
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if video:
                folder_path = os.path.join("Videos", author)
                os.makedirs(folder_path, exist_ok=True)
                video.download(output_path=folder_path)
                st.write("Downloaded:", yt.title)
            else:
                st.write("Video not available:", yt.title)
        except Exception as e:
            st.write("Error downloading video:", e)
        progress_bar.progress(i / total_videos)
    st.write("All Done")

def main():
    st.title("YouTube Playlist Downloader")
    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    if st.button("Download"):
        if playlist_url:
            download_videos(playlist_url)
        else:
            st.write("Please enter a valid playlist URL.")

if __name__ == "__main__":
    main()
