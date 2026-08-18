from pydantic import BaseModel, Field
from typing import Literal, Any


class ECGAnalysisResult(BaseModel):
    patient_id: str = Field(..., description="Patient ID")
    signal_quality: Literal["low", "medium", "high"] = Field(..., description="Signal quality")
    # TODO: heart rate
    # TODO: Rhythm-related basic measurements, PR, QRS, QT/QTc
    # TODO: intervals
    # TODO: ST-related Findings
    # TODO: Findings requiring physician review
