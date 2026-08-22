from typing import Literal, Sequence
from pydantic import BaseModel, Field, field_validator, model_validator
from wfdb import Record
import numpy as np
import math

_MIN_DURATION_SEC = 2.5


class ECGLeads(BaseModel):
    I: list[float] = Field(..., min_length=1, description="Lead I signal samples")
    II: list[float] = Field(..., min_length=1, description="Lead II signal samples")
    III: list[float] = Field(..., min_length=1, description="Lead III signal samples")
    AVR: list[float] = Field(..., min_length=1, description="Augmented vector right lead samples")
    AVL: list[float] = Field(..., min_length=1, description="Augmented vector left lead samples")
    AVF: list[float] = Field(..., min_length=1, description="Augmented vector foot lead samples")
    V1: list[float] = Field(..., min_length=1, description="Precordial lead V1 samples")
    V2: list[float] = Field(..., min_length=1, description="Precordial lead V2 samples")
    V3: list[float] = Field(..., min_length=1, description="Precordial lead V3 samples")
    V4: list[float] = Field(..., min_length=1, description="Precordial lead V4 samples")
    V5: list[float] = Field(..., min_length=1, description="Precordial lead V5 samples")
    V6: list[float] = Field(..., min_length=1, description="Precordial lead V6 samples")

    @field_validator("I", "II", "III", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6")
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

    @staticmethod
    def from_numpy(array: np.ndarray) -> "ECGLeads":
        if not isinstance(array, np.ndarray):
            raise TypeError(f"Input must be numpy.ndarray, got {type(array)}")
        if array.ndim != 2 or array.shape[0] != 12:
            raise ValueError("Array must be 2D with shape (12, n_samples)")
        if not np.isfinite(array).all():
            raise ValueError("Signal contains NaN or infinite values")

        lead_names = ["I", "II", "III", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6"]
        data = {name: array[i].astype(float).tolist() for i, name in enumerate(lead_names)}
        return ECGLeads(**data)

    def to_numpy(self) -> np.ndarray:
        return np.array(list(self.model_dump().values()))


class ECGRecord(BaseModel):
    leads: ECGLeads = Field(..., description="12-lead ECG signal data (12×N matrix)")
    patient_id: str = Field(..., min_length=1, description="Patient ID")
    sample_rate: Literal[100, 500] = Field(..., description="Sampling rate in Hz")
    units: Sequence[str] | None = Field(default=None, description="ECG units", min_length=12, max_length=12)
    metadata: dict | None = Field(description="ECG metadata")

    @model_validator(mode="after")
    def check_duration(self) -> "ECGRecord":
        n_samples = len(self.leads.I)
        duration = n_samples / self.sample_rate
        if duration < _MIN_DURATION_SEC:
            raise ValueError(f"ECG too short: {duration:.2f}s, minimum required is {_MIN_DURATION_SEC}s")
        return self

    @staticmethod
    def from_Record(rec: Record, patient_id: str, metadata: dict) -> "ECGRecord":
        leads = ECGLeads(
            **dict(zip(rec.sig_name, rec.p_signal.transpose()))
        )
        return ECGRecord(
            leads=leads,
            patient_id=patient_id,
            sample_rate=rec.fs,
            units=rec.units,
            metadata=metadata
        )

    def to_Record(self) -> Record:
        """Convert ECGRecord to a wfdb.Record object"""
        leads = self.leads.model_dump()
        sig_name = list(leads.keys())
        p_signal = np.array(list(leads.values())).transpose()
        return Record(
            sig_name=sig_name,
            p_signal=p_signal,
            fs=self.sample_rate,
            units=self.units
        )
