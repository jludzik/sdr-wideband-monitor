from config import LTE_1800, SPECTRUM_LTE, NOISE_1800, DETECTOR_1800
from radio import PlutoSDR

from ui.spectrum_plot import LiveSpectrumPlot

from dsp.spectrum import SpectrumProcessor
from dsp.noise_estimator import NoiseEstimator
from dsp.activity_detector import ActivityDetector

from data_models import SpectrumResult


def main() -> None:
    radio = PlutoSDR(LTE_1800)
    spectrum_processor = SpectrumProcessor(spectrum_config=SPECTRUM_LTE, radio_config=LTE_1800)
    noise_estimator = NoiseEstimator(noise_config=NOISE_1800, spectrum_config=SPECTRUM_LTE, radio_config=LTE_1800)
    activity_detector = ActivityDetector(activity_detector_config=DETECTOR_1800)
    plot = LiveSpectrumPlot(spectrum_processor.get_frequency_axis())

    while plot.is_open():
        # --------------- SPECTRUM -----------------------------------------
        samples = radio.receive_iq()

        spectrum_linear = spectrum_processor.compute_welch(samples, "linear")


        # --------------- NOISE FLOOR & DETECTION THRESHOLDS ---------------
        noise_floor_lin = noise_estimator.fcme(spectrum_linear.power)
        
        detection_threshold_low_lin, detection_threshold_high_lin = noise_estimator.detection_threshold(noise_floor_lin)


        # --------------- DETECTION -----------------------------------------
        final_bins = activity_detector.detect(spectrum_linear, detection_threshold_low_lin, detection_threshold_high_lin)

        
        # --------------- PLOT  ----------------------------------------------
        power_db = spectrum_processor.convert_power_to_db(spectrum_linear.power)
        spectrum_db = SpectrumResult(power=power_db, frequency_hz=spectrum_linear.frequency_hz)

        noise_floor_db = spectrum_processor.convert_power_to_db(noise_floor_lin)

        detection_threshold_high_db = spectrum_processor.convert_power_to_db(detection_threshold_high_lin)
        detection_threshold_low_db = spectrum_processor.convert_power_to_db(detection_threshold_low_lin)

        plot.update(spectrum_db, noise_floor_db, detection_threshold_high_db, detection_threshold_low_db, occupied_bins=final_bins)


        
if __name__ == "__main__":
    main()