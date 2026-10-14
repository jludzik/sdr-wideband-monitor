from config import LTE_1800, SPECTRUM_LTE
from radio import PlutoSDR
from dsp.spectrum import SpectrumProcessor
from ui.spectrum_plot import LiveSpectrumPlot
from data_models import SpectrumResult

def main() -> None:
    radio = PlutoSDR(LTE_1800)
    spectrum_processor = SpectrumProcessor(sample_rate=radio.sampling_rate, config=SPECTRUM_LTE)

    frequency_axis = spectrum_processor.get_frequency_axis(radio.center_freq)
    plot = LiveSpectrumPlot(frequency_axis)

    while plot.is_open():
        samples = radio.receiveIQ()
        spectrum = spectrum_processor.compute_welch(samples, radio.center_freq)
        plot.update(spectrum)


if __name__ == "__main__":
    main()