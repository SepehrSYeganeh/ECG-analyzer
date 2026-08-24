from pydantic import BaseModel, Field
import numpy as np
from wfdb import Annotation
from .ecg_models import ECGRecord
from .diagnosis_models import DiagnosisHeartArrhythmiaReport
from ecg_analyzer.utils import plot_ecg


class ECGAnalysisResult(BaseModel):
    filtered_record: ECGRecord = Field(..., description="Filtered ECG record")
    duration: float = Field(..., description="Duration (ms)")
    r_peaks: list[int] = Field(..., description="R-peaks indices")
    rr_intervals: list[float] = Field(..., description="RR intervals (ms)")
    instantaneous_heart_rate: list[float] = Field(..., description="Instantaneous heart rate (BPM)")
    average_heart_rate: float = Field(..., description="Average heart rate (BPM)")
    symbols: list[str] = Field(..., description="Beat symbols")
    diagnosis: DiagnosisHeartArrhythmiaReport = Field(..., description="Diagnosis heart arrhythmia")

    def to_Annotation(self) -> Annotation:
        num_channels = 12
        return Annotation(
            record_name=self.filtered_record.patient_id,
            extension="atr",
            fs=self.filtered_record.sample_rate,
            sample=np.tile(self.r_peaks, num_channels),
            symbol=self.symbols * num_channels,
            chan=np.repeat(np.arange(num_channels), len(self.r_peaks))
        )

    def plot(self):
        plot_ecg(
            ecg_record=self.filtered_record,
            annotation=self.to_Annotation(),
            title=f"Analyzed ECG Record for patient {self.filtered_record.patient_id}",
            plot_sym=True
        )
