from dataclasses import dataclass

@dataclass(frozen=True)
class SDRConfig:
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



# -------- PRESETS ----------------

LTE_1800 = SDRConfig(
    sample_rate=35_000_000,
    bandwidth=35_000_000,
    center_freq=1_872_500_000,
    gain_control_mode="manual",
    gain=55.0
)

SPECTRUM_LTE = SpectrumConfig(
    nfft=8192,
    overlap_ratio=0.25,
    processing_bandwidth=32_000_000,
    window="hamming"
)


ISM_868 = SDRConfig(
    sample_rate=4_000_000,
    bandwidth=3_000_000,
    center_freq=868_000_000,
    gain_control_mode="manual",
    gain=40.0,
)

...

# -------------------------------------