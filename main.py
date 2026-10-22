from config import LTE_1800, SPECTRUM_LTE
from radio import PlutoSDR
from dsp.spectrum import SpectrumProcessor
from ui.spectrum_plot import LiveSpectrumPlot
from dsp.noise_estimator import NoiseEstimator

def main() -> None:
    radio = PlutoSDR(LTE_1800)
    spectrum_processor = SpectrumProcessor(sample_rate=radio.sampling_rate, spectrum_config=SPECTRUM_LTE)

    frequency_axis = spectrum_processor.get_frequency_axis(radio.center_freq)
    plot = LiveSpectrumPlot(frequency_axis)

    while plot.is_open():
        samples = radio.receive_iq()
        spectrum_linear = spectrum_processor.compute_welch(samples, radio.center_freq, "linear")
        spectrum_db = spectrum_processor.convert_to_db(spectrum_linear)

        noise_floor = NoiseEstimator.percentile(spectrum_db.power, 20.0)
        plot.update(spectrum_db, noise_floor)


if __name__ == "__main__":
    main()