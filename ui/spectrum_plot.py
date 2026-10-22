import numpy as np
import matplotlib.pyplot as plt
from typing import Optional

from data_models import SpectrumResult


class LiveSpectrumPlot:
    def __init__(self,frequency_hz: np.ndarray,y_min: float = -60,y_max: float = 40) -> None:

        plt.ion()

        self._fig, self._ax = plt.subplots(figsize=(18, 5))
        freq_mhz = frequency_hz * 1e-6

        self._line, = self._ax.plot(freq_mhz, np.zeros(len(frequency_hz)), label="Signal Spectrum", color="blue")
        self._line_secondary, = self._ax.plot(freq_mhz, np.zeros(len(frequency_hz)), label="Estimated Noise Floor", color="red", linestyle="--")


        self._ax.set_xlabel("f [MHz]")
        self._ax.set_ylabel("PSD")
        self._ax.legend()
        self._ax.set_ylim(y_min,y_max)
        self._ax.grid(True)

        plt.show(block=False)


    def update(self,spectrum: SpectrumResult, secondary_y: Optional[np.ndarray] = None) -> None:

        freq_mhz = spectrum.frequency_hz * 1e-6

        self._line.set_xdata(freq_mhz)        
        self._line.set_ydata(spectrum.power)


        if secondary_y is not None:
            self._line_secondary.set_xdata(freq_mhz)
            self._line_secondary.set_ydata(secondary_y)
            self._line_secondary.set_visible(True)
        else:
            self._line_secondary.set_visible(False)

        self._ax.set_xlim(freq_mhz[0], freq_mhz[-1])

        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()

        plt.pause(0.001)


    def is_open(self) -> bool:
        return plt.fignum_exists(self._fig.number)