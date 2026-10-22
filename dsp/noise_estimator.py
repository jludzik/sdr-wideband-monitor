import numpy as np
import scipy.signal
import scipy.stats


class NoiseEstimator:
    @staticmethod
    def percentile(power: np.ndarray, percentile: float) -> np.ndarray:

        noise_floor = np.percentile(power, percentile)
        
        return np.full(np.size(power), noise_floor)

    @staticmethod
    def fcme(power: np.ndarray) -> np.ndarray:
        pass
