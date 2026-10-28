import numpy as np
from scipy.stats import gamma
from collections import deque

from config import NoiseConfig, SpectrumConfig, RadioConfig

class NoiseEstimator:
    def __init__(self, noise_config: NoiseConfig, spectrum_config: SpectrumConfig, radio_config: RadioConfig) -> None:
        self._noise_config = noise_config
        self._spectrum_config = spectrum_config
        self._buffer_size = radio_config.buffer_size

        # Calculate Welch segment count
        self._welch_segment_count = 1 + (self._buffer_size - self._spectrum_config.nfft) // (self._spectrum_config.nfft - self._spectrum_config.noverlap)

        # Calculate FCME factor
        self._fcme_factor = float(gamma.isf(0.01, a=self._welch_segment_count, scale=1 / self._welch_segment_count))

        # Calculate detection factor LOW
        self._detection_factor_low = float(gamma.isf(self._noise_config.detection_pfa_low, a=self._welch_segment_count, scale=1 / self._welch_segment_count))

        # Calculate detection factor HIGH
        self._detection_factor_high = float(gamma.isf(self._noise_config.detection_pfa_high, a=self._welch_segment_count, scale=1 / self._welch_segment_count))

        # Store noise history to calculate median over time
        self._noise_history = deque(maxlen=self._noise_config.median_length)


    def _median_over_time(self, noise_floor_linear: float) -> float:
        self._noise_history.append(float(noise_floor_linear))
        noise_median = float(np.median(self._noise_history))

        return float(noise_median)


    def reset(self) -> None:
        self._noise_history.clear()


    def detection_threshold(self, noise_floor_linear: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
            return (noise_floor_linear * self._detection_factor_low, noise_floor_linear * self._detection_factor_high)


    def fcme(self, power_linear: np.ndarray) -> np.ndarray:

        # Init starting subset
        power_len = len(power_linear)
        power_sorted = np.sort(power_linear)

        noise_cand_len = max(1, int(np.ceil(self._noise_config.fcme_initial_grp_ratio * power_len)))

        while True:
            noise_cand = power_sorted[0:noise_cand_len]
            noise_cand_mean = float(np.mean(noise_cand))

            fcme_threshold = noise_cand_mean * self._fcme_factor

            new_noise_cand_len = int(np.searchsorted(power_sorted, fcme_threshold, side="left"))

            if(new_noise_cand_len <= noise_cand_len):
                estimated_noise_floor_lin = self._median_over_time(noise_cand_mean)

                return np.full_like(power_linear, estimated_noise_floor_lin, dtype=float)

            noise_cand_len = new_noise_cand_len
