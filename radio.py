import numpy as np
import adi

from config import SDRConfig


class PlutoSDR:
    def __init__(self, config: SDRConfig) -> None:

        self._config = config
        self._sdr = adi.Pluto(config.uri)

        self._sdr.gain_control_mode_chan0 = "manual"
        self._sdr.rx_hardwaregain_chan0 = float(self._config.gain)
        self._sdr.rx_lo = int(self._config.center_freq)
        self._sdr.sample_rate = int(self._config.sample_rate)
        self._sdr.rx_rf_bandwidth = int(self._config.bandwidth)
        self._sdr.rx_buffer_size = self._config.buffer_size

        phy = self._sdr.ctx.find_device("ad9361-phy")
        rx0 = phy.find_channel("voltage0", False)
                
        rx0.attrs["bb_dc_offset_tracking_en"].value = "1"
        rx0.attrs["rf_dc_offset_tracking_en"].value = "1"
        rx0.attrs["quadrature_tracking_en"].value = "1"


    def receiveIQ(self) -> np.ndarray:
        return self._sdr.rx()


    def setCenterFreq(self, frequency_hz: int) -> None:
        self._sdr.rx_lo = int(frequency_hz)


    def setSamplingRate(self, sampling_rate: int) -> None:
        self._sdr.sample_rate = int(sampling_rate)


    def setBandwidth(self, bandwidth: int) -> None:
        self._sdr.rx_rf_bandwidth = int(bandwidth)


    @property
    def center_freq(self) -> int:
        return int(self._sdr.rx_lo)


    @property
    def sampling_rate(self) -> int:
        return int(self._sdr.sample_rate)


    @property
    def bandwidth(self) -> int:
        return int(self._sdr.rx_rf_bandwidth)