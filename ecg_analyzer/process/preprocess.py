from scipy.signal import butter, sosfiltfilt
from ecg_analyzer.models import ECGLeads


def remove_baseline_wander(
        leads: ECGLeads,
        sample_rate: int,
        cutoff_hz: float = 0.5
) -> ECGLeads:
    """
    Remove baseline wander using a zero-phase Butterworth high-pass filter at cutoff_hz (default 0.5 Hz).

    Args:
        record_path: Path to WFDB record (without extension).
        cutoff_hz:   High-pass cutoff. Keep at 0.5 Hz to preserve ST segment.

    Returns:
        filtered_signal: ECGLeads filtered signal.
    """
    sos = butter(N=4, Wn=cutoff_hz, btype='highpass', fs=sample_rate, output='sos')
    filtered_signal = sosfiltfilt(sos, leads.to_numpy())

    return ECGLeads.from_numpy(filtered_signal)
