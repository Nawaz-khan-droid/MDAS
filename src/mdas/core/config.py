from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class MDASConfig:
    language: str = "en"
    max_characters: int = 250_000
    include_token_details: bool = True
    model_dir: Path = field(default_factory=lambda: Path("models"))
