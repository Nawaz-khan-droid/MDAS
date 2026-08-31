from fastapi import APIRouter, HTTPException
from mdas.api.schemas import AnalysisRequest, AnalysisResponse, CapabilitiesResponse
from mdas.application.analysis_service import AnalysisService
import uuid

router = APIRouter()

analysis_service = None

def get_analysis_service():
    global analysis_service
    if analysis_service is None:
        analysis_service = AnalysisService("models")
    return analysis_service

@router.post("/v1/analyze", response_model=AnalysisResponse)
def analyze_text(request: AnalysisRequest):
    service = get_analysis_service()
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    try:
        result = service.analyze(request.text, str(uuid.uuid4()))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/v1/capabilities", response_model=CapabilitiesResponse)
def capabilities():
    return CapabilitiesResponse(
        language=["en"],
        features=[
            "statistics",
            "linguistics",
            "ner",
            "voice",
            "spam",
            "topic",
            "intent",
            "sentiment",
            "absa",
            "urgency",
            "churn_risk",
            "toxicity_signal",
            "sarcasm_evidence"
        ]
    )

@router.get("/health")
def health_check():
    return {"status": "online"}
