from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class ClassificationResult:
    label: str | None
    confidence: float | None
    status: str = "ok"
    model: str | None = None
    domain: str | None = None
    alternatives: list[dict[str, Any]] = field(default_factory=list)

@dataclass
class Entity:
    text: str
    label: str
    start: int
    end: int
    source: str = "spacy"

@dataclass
class AnalysisResult:
    meta: dict[str, Any]
    statistics: dict[str, Any]
    linguistics: dict[str, Any]
    classification: dict[str, Any]
    radar: dict[str, float | None]
    signals: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
