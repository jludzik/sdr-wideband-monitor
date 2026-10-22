import numpy as np
from scipy.stats import gamma
from collections import deque

from config import LTE_1800, SPECTRUM_LTE


class NoiseEstimator:
    def __init__(self, median_length: int = 5) -> None:
        self._noise_history = deque(maxlen=median_length)

    def median_over_time(self, noise_floor_linear: np.ndarray) -> np.ndarray:
        self._noise_history.append(float(noise_floor_linear[0]))

        noise_median = float(np.median(self._noise_history))

        return np.full_like(noise_floor_linear, noise_median, dtype=float)

    @staticmethod
    def percentile(power: np.ndarray, percentile: float) -> np.ndarray:
        noise_floor = np.percentile(power, percentile)
        
        return np.full(np.size(power), noise_floor)

    @staticmethod
    def fcme(power_linear: np.ndarray, initial_grp_ratio: float, nfft: int, noverlap: int, buffer_size: int) -> np.ndarray:

        # Calculate FCME factor
        welch_segment_count = 1 + (buffer_size - nfft) // (nfft - noverlap)
        fcme_factor = float(gamma.isf(0.01, a=welch_segment_count, scale=1 / welch_segment_count))

        # Init starting subset
        power_len = len(power_linear)
        power_sorted = np.sort(power_linear)

        noise_cand_len = max(1, int(np.ceil(initial_grp_ratio * power_len)))

        while True:
            noise_cand = power_sorted[0:noise_cand_len]
            noise_cand_mean = float(np.mean(noise_cand))

            fcme_threshold = noise_cand_mean * fcme_factor

            new_noise_cand_len = int(np.count_nonzero(power_sorted < fcme_threshold))

            if(new_noise_cand_len <= noise_cand_len):
                return np.full_like(power_linear, noise_cand_mean, dtype=float)

            noise_cand_len = new_noise_cand_len



    def cfar():
        pass
        
        

