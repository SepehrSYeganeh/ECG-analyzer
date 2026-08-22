import wfdb
from ecg_analyzer.models import ECGRecord


def plot_ecg(
        ecg_record: ECGRecord,
        return_fig: bool = False,
        title: str = None,
):
    """
    :param ecg_record:  ECGRecord
    :param return_fig:  If True, return a matplotlib figure
    :param title:       The title of the figure

    :return:            matplotlib figure or None
    """
    if title is None:
        title = f"ECG patient id: {ecg_record.patient_id}"
    record = ecg_record.to_Record()
    result = wfdb.plot_wfdb(
        record,
        title=title,
        return_fig=return_fig,
        ecg_grids='all',
        figsize=(16, 12)
    )
    return result
