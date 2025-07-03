import os
import json
import re
from yt_dlp import YoutubeDL

# Step 1: Create a valid filename function
def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# Step 4: Define progress hook
def progress_hook(d):
    if d['status'] == 'finished':
        info = d['info_dict']
        title = info.get('title', 'Unknown Title')
        artist = info.get('uploader', 'Unknown Artist')
        video_id = info.get('id')
        ext = info.get('ext', 'mp3')

        safe_title = clean_filename(title)
        filename = f"{safe_title}.mp3"
        original_path = f"{video_id}.{ext}"
        final_path = os.path.join(output_dir, filename)

        if os.path.exists(original_path):
            os.rename(original_path, final_path)

        # Add or update song metadata
        songs_meta[safe_title] = {
            "title": title,
            "artist": artist,
            "location": final_path
        }

# Step 5: Define YT-DLP options
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

# Step 6: Start download
playlist_url = "https://youtube.com/playlist?list=PLwi5bnlaFJvjbnvBu4aLwuGkQH4F45nUO"

if __name__ == "__main__":

    # Step 2: Prepare metadata dictionary
    songs_meta = {}

    # Load existing metadata if present
    meta_file = "songs_meta.json"
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            songs_meta = json.load(f)

    # Step 3: Define output directory
    output_dir = "songs"
    os.makedirs(output_dir, exist_ok=True)

    with YoutubeDL(get_yt_dlp_opts()) as ydl:
        ydl.download([playlist_url])

    # Step 7: Save updated metadata
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(songs_meta, f, indent=4, ensure_ascii=False)
