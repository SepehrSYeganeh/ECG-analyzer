import numpy as np
from ecg_analyzer.models import ECGRecord
from .filters import qrs_detection_bandpass
from .normalizers import z_score_normalization, rms_signal


def qrs_detection_preprocess(record: ECGRecord) -> np.ndarray:
    leads = qrs_detection_bandpass(record.leads, record.sample_rate)
    leads = z_score_normalization(leads)
    return rms_signal(leads)
