from pydantic import BaseModel, Field


class ECGLeads(BaseModel):
    I: list[float] = Field(..., description="Lead I signal samples")
    II: list[float] = Field(..., description="Lead II signal samples")
    III: list[float] = Field(..., description="Lead III signal samples")
    aVR: list[float] = Field(..., description="Augmented vector right lead samples")
    aVL: list[float] = Field(..., description="Augmented vector left lead samples")
    aVF: list[float] = Field(..., description="Augmented vector foot lead samples")
    V1: list[float] = Field(..., description="Precordial lead V1 samples")
    V2: list[float] = Field(..., description="Precordial lead V2 samples")
    V3: list[float] = Field(..., description="Precordial lead V3 samples")
    V4: list[float] = Field(..., description="Precordial lead V4 samples")
    V5: list[float] = Field(..., description="Precordial lead V5 samples")
    V6: list[float] = Field(..., description="Precordial lead V6 samples")


class ECGModel(BaseModel):
    patient_id: str = Field(..., description="Patient ID")
    sample_rate: int = Field(
        ...,
        gt=0,
        description="Sampling rate in Hz",
        examples=[500]
    )
    leads: ECGSignal = Field(
        ...,
        description="12-lead ECG signal data (12×N matrix)"
    )
