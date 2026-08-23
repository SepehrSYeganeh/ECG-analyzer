from wfdb import Annotation
from .ecg_baseline import *
from ecg_analyzer.models import ECGRecord, ECGAnalysisResult
from ecg_analyzer.preprocess.filters import (
    remove_baseline_wander,
    general_waveform_bandpass
)


def baseline_analysis(
        rms_signal: np.ndarray,
        record: ECGRecord,
) -> Annotation:
    filtered_leads = remove_baseline_wander(
        record.leads,
        record.sample_rate
    ) if record.sample_rate < 500 else general_waveform_bandpass(
        record.leads,
        record.sample_rate
    )
    filtered_record = record.model_copy(update={'leads': filtered_leads})
    duration = calc_duration(rms_signal, record.sample_rate)
    r_peaks = detect_r_peaks(rms_signal, record.sample_rate)
    rr_intervals = calc_RR_intervals(r_peaks, record.sample_rate)
    instantaneous_heart_rate = calc_instantaneous_heart_rate(rr_intervals)
    average_heart_rate = calc_average_heart_rate(r_peaks, record.sample_rate)

    # TODO: find symbols
    symbols = ['N'] * len(r_peaks)

    return ECGAnalysisResult(
        filtered_record=filtered_record,
        duration=duration,
        r_peaks=r_peaks,
        rr_intervals=rr_intervals,
        instantaneous_heart_rate=instantaneous_heart_rate,
        average_heart_rate=average_heart_rate,
        symbols=symbols
    )
