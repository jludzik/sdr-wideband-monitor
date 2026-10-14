import numpy as np
import scipy.signal

from config import SpectrumConfig
from data_models import SpectrumResult


class SpectrumProcessor:
    def __init__(self, sample_rate: int, config: SpectrumConfig) -> None:
        self._sample_rate = sample_rate
        self._config = config
        self._frequency_offset = self._create_frequency_axis()
        self._edge_mask = self._create_edge_mask()
        self._max_hold_spectrum = None


    def _create_frequency_axis(self) -> np.ndarray:
        return (np.fft.fftshift(np.fft.fftfreq(self._config.nfft,d=1 / self._sample_rate)))


    def _create_edge_mask(self) -> np.ndarray:
        return (np.abs(self._frequency_offset) <= self._config.processing_bandwidth / 2)


    def get_frequency_axis(self, center_freq: int) -> np.ndarray:
        return (self._frequency_offset[self._edge_mask] + center_freq)


    def compute_welch(self, signal: np.ndarray, center_freq: int) -> SpectrumResult:

        _, power = scipy.signal.welch(
            signal,
            fs=self._sample_rate,
            window=self._config.window,
            nperseg=self._config.nfft,
            noverlap=self._config.noverlap,
            nfft=self._config.nfft,
            return_onesided=False,
            detrend="constant",
            scaling="density"
        )

        power_db = 10 * np.log10(np.fft.fftshift(power) + 1e-24)
        frequency_hz = self.get_frequency_axis(center_freq)

        return SpectrumResult(frequency_hz=frequency_hz, power_db=power_db[self._edge_mask])


    def reset_max_hold(self) -> None:
        self._max_hold_spectrum = None


    def compute_max_hold(self, new_signal: np.ndarray, center_freq: int) -> SpectrumResult:

        new_spectrum = self.compute_welch(new_signal, center_freq)

        if((self._max_hold_spectrum is None) or not (np.array_equal(new_spectrum.frequency_hz, self._max_hold_spectrum.frequency_hz))):
            self._max_hold_spectrum = new_spectrum
        else:
            self._max_hold_spectrum.power_db = np.maximum(self._max_hold_spectrum.power_db, new_spectrum.power_db)

        return self._max_hold_spectrum

    