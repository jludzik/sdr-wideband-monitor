from config import LTE_1800, SPECTRUM_LTE
from radio import PlutoSDR
from dsp.spectrum import SpectrumProcessor
from ui.spectrum_plot import LiveSpectrumPlot
from dsp.noise_estimator import NoiseEstimator
from data_models import SpectrumResult

def main() -> None:
    radio = PlutoSDR(LTE_1800)
    spectrum_processor = SpectrumProcessor(sample_rate=radio.sampling_rate, spectrum_config=SPECTRUM_LTE)
    noise_estimator = NoiseEstimator(median_length=11)

    frequency_axis = spectrum_processor.get_frequency_axis(radio.center_freq)
    plot = LiveSpectrumPlot(frequency_axis)

    while plot.is_open():
        samples = radio.receive_iq()
        spectrum_linear = spectrum_processor.compute_welch(samples, radio.center_freq, "linear")

        power_db = spectrum_processor.convert_power_to_db(spectrum_linear.power)
        spectrum_db = SpectrumResult(power=power_db, frequency_hz=spectrum_linear.frequency_hz)

        #noise_floor = NoiseEstimator.percentile(spectrum_db.power, 20.0)
        noise_floor_lin = NoiseEstimator.fcme(spectrum_linear.power, 0.06, SPECTRUM_LTE.nfft, SPECTRUM_LTE.noverlap, len(samples))
        noise_floor_lin = noise_estimator.median_over_time(noise_floor_lin)

        noise_floor_db = spectrum_processor.convert_power_to_db(noise_floor_lin)

        plot.update(spectrum_db, noise_floor_db)

        

if __name__ == "__main__":
    main()