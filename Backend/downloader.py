import os
import re
from yt_dlp import YoutubeDL
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["shazam_db"]
songs_collection = db["songs"]

# Function to clean filenames
def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Output directory
output_dir = "songs"
os.makedirs(output_dir, exist_ok=True)

# Progress hook to handle each downloaded song
def progress_hook(d):
    if d['status'] == 'finished':
        info = d['info_dict']
        title = info.get('title', 'Unknown Title')
        artist = info.get('uploader', 'Unknown Artist')
        video_id = info.get('id')  # Unique YouTube ID
        ext = info.get('ext', 'mp3')
        webpage_url = info.get('webpage_url', '')

        safe_title = clean_filename(title)
        filename = f"{safe_title}.mp3"
        final_path = os.path.join(output_dir, filename)

        # Check if file already exists and is hashed
        existing_song = songs_collection.find_one({"video_id": video_id})
        if os.path.exists(final_path) and existing_song and existing_song.get("hash_generated", False):
            print(f"✅ Skipping '{safe_title}' — already downloaded and indexed.")
            return

        # Rename file if needed
        original_path = f"{video_id}.{ext}"
        if os.path.exists(original_path):
            os.rename(original_path, final_path)

        # Insert or update song in MongoDB
        songs_collection.update_one(
            {"video_id": video_id},
            {"$set": {
                "title": safe_title,
                "artist": artist,
                "location": final_path,
                "youtube_url": webpage_url,
                "video_id": video_id,
                "hash_generated": False
            }},
            upsert=True
        )
        print(f"🎵 Processed: {safe_title}")

# YT-DLP options
def get_yt_dlp_opts():
    return {
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'quiet': False,
        'noplaylist': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'outtmpl': '%(id)s.%(ext)s',
    }

# Playlist or video URL
playlist_url = "https://youtube.com/playlist?list=PLwi5bnlaFJvi9VOGV9btK0vHREbYi9PmZ&si=TrXWaso_hXc73zNH"

if __name__ == "__main__":
    with YoutubeDL(get_yt_dlp_opts()) as ydl:
        ydl.download([playlist_url])
