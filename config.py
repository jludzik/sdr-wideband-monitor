from dataclasses import dataclass

@dataclass(frozen=True)
class RadioConfig:
    sample_rate: int
    bandwidth: int 
    center_freq: int
    gain_control_mode: str
    gain: float

    uri: str = "ip:192.168.2.1"
    buffer_size: int = 65_536

    
@dataclass(frozen=True)
class SpectrumConfig:
    nfft: int
    overlap_ratio: float
    processing_bandwidth: int
    window: str

    @property
    def noverlap(self) -> int:
        return int(self.nfft * self.overlap_ratio)


@dataclass(frozen=True)
class NoiseConfig:
    fcme_initial_grp_ratio: float
    median_length: int
    detection_pfa_low: float
    detection_pfa_high: float

@dataclass(frozen=True)
class ActivityDetectorConfig:
    history_size: int
    required_hits: int


# -------- PRESETS ----------------

LTE_1800 = RadioConfig(
    sample_rate=35_000_000,
    bandwidth=35_000_000,
    center_freq=1_876_500_000,
    #center_freq=1_872_500_000,
    #center_freq=1_860_500_000,
    #center_freq=1_850_500_000,
    gain_control_mode="fast_attack",
    gain=45.0
)

SPECTRUM_LTE = SpectrumConfig(
    nfft=4096,
    overlap_ratio=0.4,
    processing_bandwidth=32_000_000,
    window="hamming"
)

NOISE_1800 = NoiseConfig(
    fcme_initial_grp_ratio=0.06,
    median_length=1,
    detection_pfa_low=1e-14,
    detection_pfa_high=1e-50
)

DETECTOR_1800 = ActivityDetectorConfig(
    history_size=10,
    required_hits=3
)


ISM_868 = RadioConfig(
    sample_rate=4_000_000,
    bandwidth=3_000_000,
    center_freq=868_000_000,
    gain_control_mode="manual",
    gain=40.0,
)

...

# -------------------------------------