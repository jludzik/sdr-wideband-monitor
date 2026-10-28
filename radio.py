import numpy as np
import adi

from config import RadioConfig


class PlutoSDR:
    def __init__(self, radio_config: RadioConfig) -> None:

        self._sdr = adi.Pluto(radio_config.uri)

        self._sdr.gain_control_mode_chan0 = str(radio_config.gain_control_mode)
        self._sdr.rx_hardwaregain_chan0 = float(radio_config.gain)
        self._sdr.rx_lo = int(radio_config.center_freq)
        self._sdr.sample_rate = int(radio_config.sample_rate)
        self._sdr.rx_rf_bandwidth = int(radio_config.bandwidth)
        self._sdr.rx_buffer_size = int(radio_config.buffer_size)

        phy = self._sdr.ctx.find_device("ad9361-phy")
        rx0 = phy.find_channel("voltage0", False)
                
        rx0.attrs["bb_dc_offset_tracking_en"].value = "1"
        rx0.attrs["rf_dc_offset_tracking_en"].value = "1"
        rx0.attrs["quadrature_tracking_en"].value = "1"


    def receive_iq(self) -> np.ndarray:
        return self._sdr.rx()

    @property
    def center_freq(self) -> int:
        return int(self._sdr.rx_lo)

    @center_freq.setter
    def center_freq(self, frequency_hz: int) -> None:
        self._sdr.rx_lo = int(frequency_hz)
        self._sdr.rx_destroy_buffer()

    @property
    def sampling_rate(self) -> int:
        return int(self._sdr.sample_rate)

    @sampling_rate.setter
    def sampling_rate(self, sampling_rate: int) -> None:
        self._sdr.sample_rate = int(sampling_rate)
        self._sdr.rx_destroy_buffer()

    @property
    def bandwidth(self) -> int:
        return int(self._sdr.rx_rf_bandwidth)

    @bandwidth.setter
    def bandwidth(self, bandwidth: int) -> None:
        self._sdr.rx_rf_bandwidth = int(bandwidth)

    @property
    def buffer_size(self) -> int:
        return int(self._sdr.rx_buffer_size)

    @buffer_size.setter
    def buffer_size(self, size: int) -> None:
        self._sdr.rx_buffer_size = int(size)
        self._sdr.rx_destroy_buffer()