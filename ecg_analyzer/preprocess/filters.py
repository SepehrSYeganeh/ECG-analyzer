from scipy.signal import butter, sosfiltfilt
from ecg_analyzer.models import ECGLeads


def remove_baseline_wander(
        leads: ECGLeads,
        fs: float,
        cutoff_hz: float = 0.5,
        order: int = 4
) -> ECGLeads:
    """
    Remove baseline wander using a zero-phase Butterworth high-pass filter at cutoff_hz (default 0.5 Hz).
    Use for 100 Hz signals.

    :param leads:       ECGLeads
    :param fs:          Sampling rate (Hz)
    :param cutoff_hz:   High-pass cutoff. Keep at 0.5 Hz to preserve ST segment
    :param order:       Order of the filter (4th order)

    :return:            ECGLeads filtered signal
    """
    sos = butter(N=order, Wn=cutoff_hz, btype='highpass', fs=fs, output='sos')
    filtered_signal = sosfiltfilt(sos, leads.to_numpy())
    return ECGLeads.from_numpy(filtered_signal)


def general_waveform_bandpass(
        leads: ECGLeads,
        fs: float,
        lowcut: float = 0.5,
        highcut: float = 40.0,
        order: int = 4
) -> ECGLeads:
    """
    Zero-phase band-pass filter for the general ECG waveform (0.5-40 Hz). Removes baseline wander, muscle noise,
    and high-frequency junk while preserving P, QRS, and T morphology.
    Use for 500 Hz signals.

    :param leads:   ECGLeads
    :param fs:      Sampling rate (Hz)
    :param lowcut:  Low-pass cutoff
    :param highcut: High-pass cutoff
    :param order:   Order of the filter

    :return:        ECGLeads filtered signal
    """
    if not 0 < lowcut < highcut < fs / 2:
        raise ValueError("cutoffs must satisfy 0 < lowcut < highcut < fs/2")
    sos = butter(N=order, Wn=[lowcut, highcut], btype="bandpass", fs=fs, output="sos")
    filtered_signal = sosfiltfilt(sos, leads.to_numpy())
    return ECGLeads.from_numpy(filtered_signal)


def qrs_detection_bandpass(
        leads: ECGLeads,
        fs: float,
        lowcut: float = 5.0,
        highcut: float = 20.0,
        order: int = 4
) -> ECGLeads:
    """
    Tighter band-pass copy (5-20 Hz) for QRS peak detection only. NOT for diagnosis: this attenuates slow ST/T
    morphology and trims low-frequency content that a diagnosis grade needs.

    :param leads:   ECGLeads
    :param fs:      Sampling rate (Hz)
    :param lowcut:  Low-pass cutoff
    :param highcut: High-pass cutoff
    :param order:   Order of the filter

    :return:        ECGLeads filtered signal
    """
    if not 0 < lowcut < highcut < fs / 2:
        raise ValueError("cutoffs must satisfy 0 < lowcut < highcut < fs/2")
    sos = butter(N=order, Wn=[lowcut, highcut], btype="bandpass", fs=fs, output="sos")
    filtered_signal = sosfiltfilt(sos, leads.to_numpy())
    return ECGLeads.from_numpy(filtered_signal)
