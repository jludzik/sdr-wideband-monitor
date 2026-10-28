import numpy as np
import matplotlib.pyplot as plt
from typing import Optional

from data_models import SpectrumResult


class LiveSpectrumPlot:
    def __init__(self,frequency_hz: np.ndarray,y_min: float = -80,y_max: float = 40) -> None:

        plt.ion()

        self._fig, self._ax = plt.subplots(figsize=(18, 5))
        freq_mhz = frequency_hz * 1e-6

        self._line, = self._ax.plot(freq_mhz, np.zeros(len(frequency_hz)), label="Signal Spectrum", color="blue")
        self._line_optional_1, = self._ax.plot(freq_mhz, np.zeros(len(frequency_hz)), label="Estimated Noise Floor", color="red", linestyle="--")
        self._line_optional_2, = self._ax.plot(freq_mhz, np.zeros(len(frequency_hz)), label="Detection High Threshold", color="green", linestyle="--")
        self._activity_points = self._ax.scatter([], [], s=10, color="darkorange", label="Detected Activity", zorder=3)


        self._ax.set_xlabel("f [MHz]")
        self._ax.set_ylabel("PSD [dB]")
        self._ax.legend()
        self._ax.set_ylim(y_min,y_max)
        self._ax.grid(True)

        plt.show(block=False)


    def update(self,spectrum: SpectrumResult, optional_1y: Optional[np.ndarray] = None, optional_2y: Optional[np.ndarray] = None, occupied_bins: Optional[np.ndarray] = None) -> None:

        freq_mhz = spectrum.frequency_hz * 1e-6

        self._line.set_xdata(freq_mhz)        
        self._line.set_ydata(spectrum.power)


        if optional_1y is not None:
            self._line_optional_1.set_xdata(freq_mhz)
            self._line_optional_1.set_ydata(optional_1y)
            self._line_optional_1.set_visible(True)
        else:
            self._line_optional_1.set_visible(False)


        if optional_2y is not None:
            self._line_optional_2.set_xdata(freq_mhz)
            self._line_optional_2.set_ydata(optional_2y)
            self._line_optional_2.set_visible(True)
        else:
            self._line_optional_2.set_visible(False)    


        if occupied_bins is not None:
            points = np.column_stack((freq_mhz[occupied_bins], spectrum.power[occupied_bins]))
            self._activity_points.set_offsets(points)
        else:
            self._activity_points.set_offsets(np.empty((0, 2)))


        self._ax.set_xlim(freq_mhz[0], freq_mhz[-1])

        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()

        plt.pause(0.001)


    def is_open(self) -> bool:
        return plt.fignum_exists(self._fig.number)