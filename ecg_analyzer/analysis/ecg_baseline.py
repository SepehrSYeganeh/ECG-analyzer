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

    dynamic_threshold = np.mean(rms_signal) + 2 * np.std(rms_signal)

    r_peaks, properties = find_peaks(
        rms_signal,
        distance=min_distance,
        height=dynamic_threshold,
        prominence=1
    )

    return r_peaks


def calc_duration(
        rms_signal: np.ndarray,
        sample_rate: float
) -> float:
    """
    Calculates the duration of the ECG signal in ms.
    """
    return len(rms_signal) / sample_rate * 1000


def calc_RR_intervals(
        r_peaks: np.ndarray,
        sample_rate: float
) -> np.ndarray:
    """
    Calculate RR intervals in ms
    """
    return np.diff(r_peaks) / sample_rate * 1000


def calc_instantaneous_heart_rate(rr_intervals: np.ndarray) -> np.ndarray:
    """
    Calculate the instantaneous heart rate in BPM.
    :param rr_intervals: rr intervals in ms.
    """
    return 60000 / rr_intervals


def calc_average_heart_rate(
        r_peaks: np.ndarray,
        sample_rate: float
) -> np.ndarray:
    """
    Calculate the average heart rate in BPM.
    """
    num_beats = len(r_peaks) - 1
    total_time_sec = (r_peaks[-1] - r_peaks[0]) / sample_rate
    return 60 * num_beats / total_time_sec
