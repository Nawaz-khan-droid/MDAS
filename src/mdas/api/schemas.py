from typing import List, Optional
from pydantic import BaseModel, Field, validator
from mdas.core.constants import MAX_TEXT_LENGTH

class LanguageResult(BaseModel):
    code: str
    label: str
    confidence: Optional[float] = None
    method: str

class UnsupportedLanguageResponse(BaseModel):
    status: str = "unsupported_language"
    language: LanguageResult
    message: str

class StatisticsResult(BaseModel):
    words: int
    characters: int
    sentences: int
    tokens: int
    paragraphs: int
    reading_time: str

class SentimentResult(BaseModel):
    label: str
    score: float
    method: str

class ClassificationCandidate(BaseModel):
    model: str
    label: str
    confidence: float

class ClassificationResult(BaseModel):
    label: str
    confidence: Optional[float] = None
    method: str
    model_version: str
    candidates: List[ClassificationCandidate] = []

class VoiceEvidence(BaseModel):
    text: str
    subject: Optional[str] = None
    verb: Optional[str] = None
    aux: Optional[str] = None
    object: Optional[str] = None
    agent: Optional[str] = None
    copula: Optional[str] = None
    complement: Optional[str] = None

class VoiceSegment(BaseModel):
    text: str
    label: str
    evidence: VoiceEvidence

class VoiceResult(BaseModel):
    summary_label: str
    method: str
    sentences: List[VoiceSegment] = Field(default_factory=list)

class EntityResult(BaseModel):
    text: str
    label: str

class LinguisticsResult(BaseModel):
    voice: VoiceResult
    entities: List[EntityResult] = Field(default_factory=list)

class AspectResult(BaseModel):
    aspect: str
    descriptor: str
    sentiment: str

class RadarSignals(BaseModel):
    sentiment: float
    urgency: float
    churn_risk: float
    sarcasm: float
    toxicity: float

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    language: LanguageResult
    statistics: StatisticsResult
    linguistics: LinguisticsResult
    sentiment: SentimentResult
    spam: ClassificationResult
    absa: List[AspectResult] = Field(default_factory=list)
    radar: RadarSignals

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=MAX_TEXT_LENGTH)

class CapabilitiesResponse(BaseModel):
    language: List[str]
    features: List[str]
