import json
import os
from fingerprint import generate_hashes, generate_constellation_map

songsMeta = {}
hashIndex = {}

with open('songs_meta.json', 'r', encoding='utf-8') as f:
    songsMeta = json.load(f)

"""with open('hash_index.json', 'r', encoding='utf-8') as f:
    hashIndex = json.load(f)"""

hash_file = "hash_index.json"
if os.path.exists(hash_file) and os.path.getsize(hash_file) > 0:
    with open(hash_file, "r", encoding="utf-8") as f:
        songs_meta = json.load(f)

for song in songsMeta.values():
    if not song["hash_generated"]:
        constellation_map = generate_constellation_map(song["location"])
        hashes = generate_hashes(constellation_map)
        song["hash_generated"]= True
        for h,t in hashes:
            if h not in hashIndex:
                hashIndex[h]=[(song["title"],t)]
            else:
                hashIndex[h].append((song["title"], t))

with open('hash_index.json', 'w', encoding='utf-8') as f:
    json.dump(hashIndex, f, indent=4)
with open('songs_meta.json', 'w', encoding='utf-8') as f:
    json.dump(songsMeta, f, indent=4)