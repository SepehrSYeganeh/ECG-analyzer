import wfdb
from pathlib import Path
from ecg_analyzer.models import ECGRecord, ECGLeads


def load_ecg_file(
        rec_path: Path,
        patient_id: str,
        metadata: dict = None
) -> ECGRecord:
    """
    :param rec_path: path to ecg record file. Both file.dat and file.hea must be in same directory.
    :param patient_id:
    :param metadata:
    :return: ECGRecord
    """
    rec = wfdb.rdrecord(rec_path)
    leads = ECGLeads(
        **dict(zip(rec.sig_name, rec.p_signal.transpose()))
    )

    ecg_rec = ECGRecord(
        leads=leads,
        patient_id=patient_id,
        sample_rate=rec.fs,
        units=rec.units,
        metadata=metadata
    )

    return ecg_rec
