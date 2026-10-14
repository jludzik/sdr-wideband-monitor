from dataclasses import dataclass
import numpy as np


@dataclass
class SpectrumResult:
    frequency_hz: np.ndarray
    power_db: np.ndarray