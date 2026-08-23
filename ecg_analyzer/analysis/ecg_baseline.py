import numpy as np
from scipy.signal import find_peaks


def detect_r_peaks(
        rms_signal: np.ndarray,
        fs: float
) -> np.ndarray:
    """
    Detects R-peaks from the 1D spatial RMS signal.

    :param rms_signal: 1D numpy array of the preprocessed RMS signal.
    :param fs: Sampling frequency of the ECG signal in Hz.

    :return r_peaks: Array containing the sample indices of the detected R-peaks.
    """
    # Refractory Period (Distance limit)
    # Physiologically, a new QRS complex cannot occur within ~200 ms of the previous one.
    refractory_period_ms = 200
    min_distance = int((refractory_period_ms / 1000.0) * fs)

    dynamic_threshold = np.mean(rms_signal) + 0.5 * np.std(rms_signal)

    r_peaks, properties = find_peaks(
        rms_signal,
        distance=min_distance,
        height=dynamic_threshold,
        prominence=0.5
    )

    # TODO: filter false peaks based on prominence

    return r_peaks
