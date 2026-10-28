from dataclasses import dataclass
import numpy as np

@dataclass
class SpectrumResult:
    frequency_hz: np.ndarray
    power: np.ndarray

@dataclass
class DetectedTransmission:
    f_start_hz: float
    f_end_hz: float
    badtwidth_hz: float
