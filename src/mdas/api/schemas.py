from typing import List, Optional
from pydantic import BaseModel, Field

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
    confidence: float
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

class UrgencyResult(BaseModel):
    label: str
    score: float
    method: str
    evidence: List[str] = Field(default_factory=list)

class ChurnResult(BaseModel):
    label: str
    score: float
    method: str
    evidence: List[str] = Field(default_factory=list)

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    language: LanguageResult
    statistics: StatisticsResult
    linguistics: LinguisticsResult
    sentiment: SentimentResult
    spam: ClassificationResult
    intent: ClassificationResult
    absa: List[AspectResult] = Field(default_factory=list)
    urgency: UrgencyResult
    churn: ChurnResult

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000)

class CapabilitiesResponse(BaseModel):
    language: List[str]
    features: List[str]
