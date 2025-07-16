import numpy as np
import librosa
from scipy.ndimage import maximum_filter, gaussian_filter
from fingerprint import generate_hashes
from collections import defaultdict
import heapq

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shazam_db"]
songs_collection = db["songs"]
hashes_collection = db["hashes"]

hashes_collection.create_index("hash")

def SearchSong(songLocation):
    y, sr = librosa.load(songLocation, sr=None)

    # STFT and spectrogram processing
    n_fft = 2048
    hop_length = 512
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_mag = np.abs(S)
    S_smooth = gaussian_filter(S_mag, sigma=1.0)

    # Peak detection
    neighborhood_size = 20
    local_max = maximum_filter(S_smooth, size=neighborhood_size) == S_smooth
    threshold = np.percentile(S_smooth[local_max], 95)
    peak_mask = local_max & (S_smooth >= threshold)
    peak_indices = np.argwhere(peak_mask)

    peak_freqs = peak_indices[:, 0] * (sr / n_fft)
    peak_times = peak_indices[:, 1] * (hop_length / sr)
    constellation_map = list(zip(peak_times, peak_freqs))

    fingerprint = generate_hashes(constellation_map)

    score = defaultdict(int)
    hash_tquery = defaultdict(list)
    for h, t in fingerprint:
        hash_tquery[h].append(t)

    hash_docs = hashes_collection.find(
        {"hash": {"$in": list(hash_tquery.keys())}},
        {"hash": 1, "time": 1, "title": 1, "_id": 0}
    )

    for doc in hash_docs:
        t_db = doc['time']
        song = doc['title']
        for t_query in hash_tquery[doc['hash']]:
            delta = round(t_db - t_query, 2)
            score[(song, delta)] += 1

    if not score:
        return []

    # Step 1: Get top 3 (song, delta) entries
    top_3 = heapq.nlargest(3, score.items(), key=lambda x: x[1])

    # Step 2: Combine scores by song
    combined = defaultdict(int)
    for (song, _), count in top_3:
        combined[song] += count

    total_score = sum(combined.values())

    # Step 3: Compute probabilities
    result = []
    for song, count in combined.items():
        probability = round((count / total_score) * 100, 2)
        result.append((song, count, probability))

    # Step 4: Return only one if confidence is 90%+
    if len(result) > 1:
        top_result = max(result, key=lambda x: x[2])
        if top_result[2] >= 90:
            result = [top_result]

    # Step 5: Return full metadata
    final = []
    for song, count, prob in result:
        meta = songs_collection.find_one({"title": song})
        if meta:
            final.append({
                "title": meta["title"],
                "artist": meta["artist"],
                "youtube_url": meta["youtube_url"],
                "confidence": prob
            })

    return final

if __name__ == "__main__":
    songAddr = "../Testsongs/Madira Noisy.mp3"
    matches = SearchSong(songAddr)
    if matches:
        for match in matches:
            print(f"\n✅ Matched: {match['title']}")
            print(f"🎤 Artist: {match['artist']}")
            print(f"🔗 YouTube: {match['youtube_url']}")
            print(f"📊 Confidence: {match['confidence']}%")
    else:
        print("❌ No match found.")
