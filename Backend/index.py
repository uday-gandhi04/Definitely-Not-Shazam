from pymongo import MongoClient
from fingerprint import generate_hashes, generate_constellation_map
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["shazam_db"]
songs_collection = db["songs"]
hashes_collection = db["hashes"]

# Load song metadata
with open("songs_meta.json", "r", encoding="utf-8") as f:
    songs_meta = json.load(f)

for song_id, song in songs_meta.items():
    if not song.get("hash_generated", False):
        print(f"Processing: {song['title']}")

        # Generate constellation map and hashes
        constellation_map = generate_constellation_map(song["location"])
        hashes = generate_hashes(constellation_map)

        # Insert hashes into DB
        for h, t in hashes:
            hashes_collection.insert_one({
                "hash": h,
                "time": t,
                "title": song["title"]
            })

        # Update song document in MongoDB
        songs_collection.update_one(
            {"title": song["title"]},
            {"$set": {
                "artist": song["artist"],
                "location": song["location"],
                "hash_generated": True
            }},
            upsert=True
        )

        # Also update in the local copy so we can save back to JSON if needed
        song["hash_generated"] = True

# Optional: Save updated metadata locally too (if you're keeping the file for any reason)
with open("songs_meta.json", "w", encoding="utf-8") as f:
    json.dump(songs_meta, f, indent=4, ensure_ascii=False)
