from dataclasses import dataclass

@dataclass(frozen=True)
class SDRConfig:

    uri: str = "ip:192.168.2.1"
    buffer_size: int = 131_072

    sample_rate: int = 35_000_000
    bandwidth: int = 35_000_000
    center_freq: int = 1_872_500_000
    gain: float = 50.0

    
@dataclass(frozen=True)
class SpectrumConfig:

    nfft: int = 8192
    overlap_ratio: float = 0.25
    processing_bandwidth: int = 30_000_000
    window: str = "hamming"

    @property
    def noverlap(self) -> int:
        return int(self.nfft * self.overlap_ratio)



# -------- PRESETS ----------------

LTE_1800 = SDRConfig(
    sample_rate=35_000_000,
    bandwidth=35_000_000,
    center_freq=1_872_500_000,
    gain=55.0
)   

ISM_868 = SDRConfig(
    sample_rate=4_000_000,
    bandwidth=3_000_000,
    center_freq=868_000_000,
    gain=40.0,
)

SPECTRUM_LTE = SpectrumConfig(
    nfft=8192,
    overlap_ratio=0.25,
    processing_bandwidth=30_000_000,
    window="hamming"
)

# -------------------------------------