import numpy as np
import matplotlib.pyplot as plt

from data_models import SpectrumResult


class LiveSpectrumPlot:
    def __init__(self,frequency_hz: np.ndarray,y_min: float = -80,y_max: float = 50) -> None:

        plt.ion()

        self._fig, self._ax = plt.subplots(figsize=(18, 5))
        self._line, = self._ax.plot(frequency_hz * 1e-6,np.zeros(len(frequency_hz)))

        self._ax.set_xlabel("f [MHz]")
        self._ax.set_ylabel("PSD [dB]")

        self._ax.set_ylim(y_min,y_max)
        self._ax.grid(True)

        plt.show(block=False)


    def update(self,spectrum: SpectrumResult) -> None:

        self._line.set_xdata(spectrum.frequency_hz*1e-6)        
        self._line.set_ydata(spectrum.power_db)

        self._ax.set_xlim(spectrum.frequency_hz[0] * 1e-6, spectrum.frequency_hz[-1] * 1e-6)

        self._fig.canvas.draw_idle()
        self._fig.canvas.flush_events()

        plt.pause(0.001)


    def is_open(self) -> bool:
        return plt.fignum_exists(self._fig.number)