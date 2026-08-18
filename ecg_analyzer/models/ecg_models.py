from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator
import math

_MIN_DURATION_SEC = 2.5


class ECGLeads(BaseModel):
    I: list[float] = Field(..., min_length=1, description="Lead I signal samples")
    II: list[float] = Field(..., min_length=1, description="Lead II signal samples")
    III: list[float] = Field(..., min_length=1, description="Lead III signal samples")
    aVR: list[float] = Field(..., min_length=1, description="Augmented vector right lead samples")
    aVL: list[float] = Field(..., min_length=1, description="Augmented vector left lead samples")
    aVF: list[float] = Field(..., min_length=1, description="Augmented vector foot lead samples")
    V1: list[float] = Field(..., min_length=1, description="Precordial lead V1 samples")
    V2: list[float] = Field(..., min_length=1, description="Precordial lead V2 samples")
    V3: list[float] = Field(..., min_length=1, description="Precordial lead V3 samples")
    V4: list[float] = Field(..., min_length=1, description="Precordial lead V4 samples")
    V5: list[float] = Field(..., min_length=1, description="Precordial lead V5 samples")
    V6: list[float] = Field(..., min_length=1, description="Precordial lead V6 samples")

    @field_validator("I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6")
    @classmethod
    def no_nan_or_inf(cls, v: list[float]) -> list[float]:
        if any(math.isnan(x) or math.isinf(x) for x in v):
            raise ValueError("Signal contains NaN or infinite values (corrupted ECG)")
        return v

    @model_validator(mode="after")
    def equal_length_leads(self) -> "ECGLeads":
        lengths = {name: len(getattr(self, name)) for name in self.model_fields}
        if len(set(lengths.values())) > 1:
            raise ValueError(f"All 12 leads must have equal sample length, got: {lengths}")
        return self


class ECGModel(BaseModel):
    patient_id: str = Field(..., min_length=1, description="Patient ID")
    sample_rate: Literal[100, 500] = Field(..., description="Sampling rate in Hz")
    leads: ECGLeads = Field(..., description="12-lead ECG signal data (12×N matrix)")

    @model_validator(mode="after")
    def check_duration(self) -> "ECGModel":
        n_samples = len(self.leads.I)
        duration = n_samples / self.sample_rate
        if duration < _MIN_DURATION_SEC:
            raise ValueError(f"ECG too short: {duration:.2f}s, minimum required is {_MIN_DURATION_SEC}s")
        return self
