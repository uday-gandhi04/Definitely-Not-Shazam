import numpy as np
import librosa
from scipy.ndimage import maximum_filter, gaussian_filter
from fingerprint import generate_hashes
from collections import defaultdict

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db=client["shazam_db"]
songs_collection=db["songs"]
hashes_collection=db["hashes"]

hashes_collection.create_index("hash")

def SearchSong(songLocation):
    """
    Search for a song by title and artist.
    Returns the fingerprints if found, else None.
    """
    # Step 1: Load the song

    y, sr = librosa.load(songLocation, sr=None)

    # Step 2: Compute STFT
    n_fft = 2048
    hop_length = 512
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_mag = np.abs(S)

    # Step 3: Smooth spectrogram (optional, helps with noisy peaks)
    S_smooth = gaussian_filter(S_mag, sigma=1.0)

    # Step 4: 2D local maxima detection
    neighborhood_size = 20
    local_max = maximum_filter(S_smooth, size=neighborhood_size) == S_smooth

    # Step 5: Apply a threshold to keep only strong peaks
    threshold = np.percentile(S_smooth[local_max], 95)  # keep top 5%
    peak_mask = local_max & (S_smooth >= threshold)

    # Step 6: Get peak coordinates (freq_bin, time_bin)
    peak_indices = np.argwhere(peak_mask)

    # Step 7: Convert to time (sec) and frequency (Hz)
    peak_freqs = peak_indices[:, 0] * (sr / n_fft)
    peak_times = peak_indices[:, 1] * (hop_length / sr)

    # Combine for (time, freq) tuples
    constellation_map = list(zip(peak_times, peak_freqs))

    #get fingerprints
    fingerprint = generate_hashes(constellation_map)
    score={
    }

    hashes = []
    hash_tquery = defaultdict(list)

    for h, t in fingerprint:
        hashes.append(h)
        hash_tquery[h].append(t)

    hash_docs=hashes_collection.find({"hash":{"$in":hashes}},{"hash":1,"time":1,"title":1,"_id":0})
    
    for doc in hash_docs:
        t_db = doc['time']
        song = doc['title']
        for t_query in hash_tquery[doc['hash']]:
            delta = round(t_db - t_query, 2)
            score[(song, delta)] = score.get((song, delta), 0) + 1
    best_match = None
    best_score = 0

    for (song, delta), count in score.items():
        if best_match is None or count > best_score:
            best_match = song
            best_score = count
    

    return best_match, songs_collection.find_one({"title":best_match}) if best_match else None

if __name__ =="__main__":
    songAddr="..\\Testsongs\\Madira Noisy.mp3"

    best_match,songsMeta=SearchSong(songAddr)
    print()
    if songsMeta:
        print("Title ",songsMeta["title"])
        print("Artist ",songsMeta["artist"])
        print("YouTube URL: ", songsMeta["youtube_url"])
    else:
        print("No match found.")
