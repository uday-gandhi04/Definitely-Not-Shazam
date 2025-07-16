from pymongo import MongoClient
from fingerprint import generate_hashes, generate_constellation_map
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["shazam_db"]
songs_collection = db["songs"]
hashes_collection = db["hashes"]

hashes_collection.create_index(
    [("hash", 1), ("time", 1), ("title", 1)],
    unique=True
)

for song in songs_collection.find():
    if not song.get("hash_generated", False):
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



