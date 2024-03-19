from flask import Flask, render_template, request
from pytube import Playlist, YouTube
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    playlist_url = request.form["playlist_url"]
    if playlist_url:
        try:
            pl = Playlist(playlist_url)
            total_videos = len(pl.video_urls)
            videos_downloaded = 0
            for video_url in pl.video_urls:
                try:
                    yt = YouTube(video_url)
                    author = yt.author.replace("/", "_").replace(":", "_")  # Sanitize author name
                    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                    if video:
                        folder_path = os.path.join("Videos", author)
                        os.makedirs(folder_path, exist_ok=True)
                        video.download(output_path=folder_path)
                        videos_downloaded += 1
                except Exception as e:
                    print("Error downloading video:", e)
            return render_template("download.html", videos_downloaded=videos_downloaded, total_videos=total_videos)
        except Exception as e:
            return render_template("error.html", error_message=str(e))
    else:
        return render_template("error.html", error_message="Please enter a valid playlist URL.")

if __name__ == "__main__":
    app.run(debug=True)
