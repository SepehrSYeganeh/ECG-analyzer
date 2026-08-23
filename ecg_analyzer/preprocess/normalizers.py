import numpy as np
from ecg_analyzer.models import ECGLeads


def z_score_normalization(leads: ECGLeads) -> ECGLeads:
    """
    Compute the z-score for each lead.

    :param leads:
    :return:
    """
    x = leads.to_numpy()
    mean = x.mean(axis=1, keepdims=True)
    std = x.std(axis=1, keepdims=True)
    return ECGLeads.from_numpy((x - mean) / std)


def rms_signal(leads: ECGLeads) -> np.ndarray:
    """
    Compute the RMS across leads for each time sample.

    :param leads:
    :return:
    """
    x = leads.to_numpy()
    return np.sqrt(np.mean(x ** 2, axis=0))
