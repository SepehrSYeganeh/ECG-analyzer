import numpy as np
from wfdb import Annotation
from .ecg_baseline import detect_r_peaks
from ecg_analyzer.models import ECGRecord


def baseline_analysis(
        rms_signal: np.ndarray,
        record: ECGRecord,
) -> Annotation:
    r_peaks = detect_r_peaks(rms_signal, record.sample_rate)

    # TODO: find symbols
    symbols = ['N'] * len(r_peaks)

    num_channels = 12
    return Annotation(
        record_name=record.patient_id,
        extension="atr",
        fs=record.sample_rate,
        sample=np.tile(r_peaks, num_channels),
        symbol=symbols * num_channels,
        chan=np.repeat(np.arange(num_channels), len(r_peaks))
    )
