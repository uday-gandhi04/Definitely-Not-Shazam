from pymongo import MongoClient
from fingerprint import generate_hashes, generate_constellation_map
from pymongo.errors import DuplicateKeyError
import os

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_URI"))
db = client["shazam_db"]
songs_collection = db["songs"]
hashes_collection = db["hashes"]

hashes_collection.create_index(
    [("hash", 1), ("time", 1), ("title", 1)],
    unique=True
)

DELETE_SONG_AFTER_HASHING = True

def index_new_songs():
    for song in songs_collection.find({"hash_generated": False}):
        # Generate constellation map and hashes
        constellation_map = generate_constellation_map(song["location"])
        hashes = generate_hashes(constellation_map)

        # Insert hashes into DB
        for h, t in hashes:
            try:
                hashes_collection.insert_one({
                    "hash": h,
                    "time": t,
                    "title": song["title"]
                })
            except DuplicateKeyError:
                pass  # Duplicate, skip

        # Update song document in MongoDB
        songs_collection.update_one(
            {"title": song["title"]},
            {"$set": {
                "hash_generated": True
            }},
        )

        try:
            if DELETE_SONG_AFTER_HASHING and os.path.exists(song["location"]):
                os.remove(song["location"])
        except Exception as e:
            print(f"Error deleting file {song['location']}: {e}")

if __name__ == "__main__":
    index_new_songs()