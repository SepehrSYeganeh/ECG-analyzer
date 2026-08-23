from pydantic import BaseModel, Field
from typing import Literal, Any
from wfdb import Annotation
from .ecg_models import ECGRecord


class ECGAnalysisResult(BaseModel):
    patient_id: str = Field(..., description="Patient ID")
    record: ECGRecord = Field(..., description="ECG record")
    ann: Annotation = Field(..., description="Annotation")
    # TODO: signal_quality: Literal["low", "medium", "high"] = Field(..., description="Signal quality")
    # TODO: heart rate
    # TODO: Rhythm-related basic measurements, PR, QRS, QT/QTc
    # TODO: intervals
    # TODO: ST-related Findings
    # TODO: Findings requiring physician review
