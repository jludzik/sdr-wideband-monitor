import numpy as np
from scipy.ndimage import label
from collections import deque

from config import ActivityDetectorConfig
from data_models import SpectrumResult

class ActivityDetector:
    def __init__(self, activity_detector_config: ActivityDetectorConfig) -> None:
        self._activity_detector_config = activity_detector_config

        self._history = deque(maxlen=self._activity_detector_config.history_size)
        self._frequency_hz = None


    def reset(self) -> None:
        self._history.clear()
        self._frequency_hz = None


    def confirm_over_time(self, occupied_bins: np.ndarray, frequency_hz: np.ndarray) -> np.ndarray:

        if self._frequency_hz is None or not np.array_equal(self._frequency_hz, frequency_hz):
            self.reset()
            self._frequency_hz = frequency_hz.copy()
            
        self._history.append(occupied_bins.copy())
        hits = np.count_nonzero(self._history, axis=0)

        return hits >= self._activity_detector_config.required_hits


    def lad(self, candidate_freq_bins: np.ndarray, strong_freq_bins: np.ndarray) -> np.ndarray:
        freq_group_ids, _ = label(candidate_freq_bins)
        freq_group_confirmed = np.unique(freq_group_ids[strong_freq_bins])
        freq_group_confirmed = freq_group_confirmed[freq_group_confirmed != 0]

        return np.isin(freq_group_ids, freq_group_confirmed)


    def detect(self, spectrum_lin: SpectrumResult, det_thrs_low_lin: np.ndarray, det_thrs_high_lin: np.ndarray) -> np.ndarray:
        candidate_bins = spectrum_lin.power > det_thrs_low_lin
        strong_bins = spectrum_lin.power > det_thrs_high_lin

        occuipied_bins = self.lad(candidate_bins, strong_bins)

        time_confirmed_bins = self.confirm_over_time(occuipied_bins, spectrum_lin.frequency_hz)

        final_bins = occuipied_bins & time_confirmed_bins

        return final_bins