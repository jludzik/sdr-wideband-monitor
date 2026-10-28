import numpy as np
import scipy.signal

from config import SpectrumConfig, RadioConfig
from data_models import SpectrumResult


class SpectrumProcessor:
    def __init__(self, spectrum_config: SpectrumConfig, radio_config: RadioConfig) -> None:
        self._spectrum_config = spectrum_config
        
        self._sample_rate = radio_config.sample_rate
        self._center_freq = radio_config.center_freq

        self._frequency_offset = self._create_frequency_axis()
        self._edge_mask = self._create_edge_mask()
        self._max_hold_spectrum = None


    def _create_frequency_axis(self) -> np.ndarray:
        return (np.fft.fftshift(np.fft.fftfreq(self._spectrum_config.nfft,d=1 / self._sample_rate)))


    def _create_edge_mask(self) -> np.ndarray:
        return (np.abs(self._frequency_offset) <= self._spectrum_config.processing_bandwidth / 2)


    def get_frequency_axis(self) -> np.ndarray:
        return (self._frequency_offset[self._edge_mask] + self._center_freq)


    def compute_welch(self, signal: np.ndarray, type: str) -> SpectrumResult:

        _, power = scipy.signal.welch(
            signal,
            fs=self._sample_rate,
            window=self._spectrum_config.window,
            nperseg=self._spectrum_config.nfft,
            noverlap=self._spectrum_config.noverlap,
            nfft=self._spectrum_config.nfft,
            return_onesided=False,
            detrend="constant",
            scaling="density"
        )

        if(type == "linear"):
            power = np.fft.fftshift(power)
        elif(type == "dB"):
            power = 10 * np.log10(np.fft.fftshift(power) + 1e-24)
        else:
            print(type)
            power = np.zeros(self._spectrum_config.nfft)
           
        frequency_hz = self.get_frequency_axis()

        return SpectrumResult(frequency_hz=frequency_hz, power=power[self._edge_mask])


    def convert_power_to_db(self, power: np.ndarray) -> np.ndarray:
        return (10 * np.log10(power + 1e-24))

        
    def compute_max_hold(self, power: np.ndarray, type: str) -> SpectrumResult:

        new_spectrum = self.compute_welch(power, self._center_freq, type)

        if((self._max_hold_spectrum is None) or not (np.array_equal(new_spectrum.frequency_hz, self._max_hold_spectrum.frequency_hz))):
            self._max_hold_spectrum = new_spectrum
        else:
            self._max_hold_spectrum.power = np.maximum(self._max_hold_spectrum.power, new_spectrum.power)

        return self._max_hold_spectrum

    def reset_max_hold(self) -> None:
            self._max_hold_spectrum = None

    