"""Single source of truth for MDAS configuration constants."""

# Maximum input text length in characters.
# Used by: Pydantic schema, AnalysisService, UI counter, API docs, tests, README
MAX_TEXT_LENGTH = 5000

# Default model directory
DEFAULT_MODEL_DIR = "models"

# Allowed tasks for production inference (no PyTorch dependencies)
PRODUCTION_TASKS = ["spam"]
