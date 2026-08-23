from pathlib import Path
from ecg_analyzer.io import load_ecg_file
from ecg_analyzer.preprocess import qrs_detection_preprocess
from ecg_analyzer.analysis import baseline_analysis
from ecg_analyzer.utils import plot_ecg


def ecg_baseline_analysis(
        rec_path: Path | str,
        rec_name: Path | str,
        patient_id: str,
        metadata: dict = None
):
    record = load_ecg_file(rec_path, rec_name, patient_id, metadata)
    rms_sig = qrs_detection_preprocess(record)
    ann = baseline_analysis(rms_sig, record)
    plot_ecg(
        ecg_record=record,
        annotation=ann,
        title="R peaks"
    )
