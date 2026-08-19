import wfdb
from pathlib import Path
from ecg_analyzer.models import ECGRecord, ECGLeads


def load_ecg_file(
        rec_path: Path | str,
        rec_name: Path | str,
        patient_id: str,
        metadata: dict = None
) -> ECGRecord:
    """
    :param rec_path: path to ecg record file
    :param rec_name: name of ecg record (without extension)
    :param patient_id:
    :param metadata:
    :return: ECGRecord
    """
    base_path = Path(rec_path) / Path(rec_name)
    dat_file = Path(f"{base_path}.dat")
    hea_file = Path(f"{base_path}.hea")

    if not hea_file.is_file():
        raise FileNotFoundError(f".hea file not found: {hea_file}")

    if not dat_file.is_file():
        raise FileNotFoundError(f".dat file not found: {dat_file}")

    rec = wfdb.rdrecord(base_path)

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
