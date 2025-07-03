import hashlib
import numpy as np
import librosa
from scipy.ndimage import maximum_filter, gaussian_filter

def generate_hashes(peaks, fan_value=5):
    """
    Generate landmark hashes from peaks.
    Each hash is made from (freq1, freq2, delta_time), anchored at time1.
    """
    hashes = []
    peaks = sorted(peaks)  # Sort by time

    for i in range(len(peaks)):
        t1, f1 = peaks[i]

        for j in range(1, fan_value + 1):
            if i + j < len(peaks):
                t2, f2 = peaks[i + j]

                delta_t = t2 - t1
                if 0 < delta_t <= 5.0:  # Limit max time delta for compact hashes
                    # Create hash string
                    hash_str = f"{int(f1)}|{int(f2)}|{int(delta_t * 100)}"
                    h = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()[0:20]  # Shorten for space
                    hashes.append((h, t1))  # Store hash + anchor time

    return hashes

def generate_constellation_map(location):
    y, sr = librosa.load(location, sr=None)

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

    return constellation_map

