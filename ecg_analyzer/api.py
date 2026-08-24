from fastapi import FastAPI, APIRouter
from ecg_analyzer.models import ECGRecord, ECGAnalysisResult
from ecg_analyzer.preprocess import qrs_detection_preprocess
from ecg_analyzer.analysis import baseline_analysis

app = FastAPI()

router = APIRouter()

app.include_router(router)


@router.post("/ecg/analyze", response_model=ECGAnalysisResult)
def analyze_ecg_record(record: ECGRecord) -> ECGAnalysisResult:
    rms_sig = qrs_detection_preprocess(record)
    return baseline_analysis(rms_sig, record)
