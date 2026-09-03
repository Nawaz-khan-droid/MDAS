"""V2 spam prediction with margin-based triage.

V1 (TextClassifier/LinearSVC) only hard-labels spam/ham with no confidence.
V2 uses the LinearSVC decision margin with a |margin| <= TRIAGE_MARGIN window
to emit 'needs_human_triage' instead of a hard call. This cuts ham->spam
false positives on e-commerce prose (domain shift) at a small spam-recall cost.

Model artifact: v2/models/spam_v2.joblib + spam_v2.json (traceability metadata).
Version: 2.0
"""
import hashlib
import json
import logging
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_MODEL = Path(__file__).resolve().parent / "models" / "spam_v2.joblib"
DEFAULT_META = Path(__file__).resolve().parent / "models" / "spam_v2.json"
TRIAGE_MARGIN = 0.2
_HASH_PREFIX_LEN = 16  # verify first 16 hex chars of SHA-256


def _verify_model_hash(model_path: Path, expected_prefix: str) -> bool:
    """Verify model file SHA-256 prefix matches metadata. Returns True if valid."""
    sha256 = hashlib.sha256()
    with open(model_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    actual = sha256.hexdigest()
    if not actual.startswith(expected_prefix.lower()):
        logger.error("Model hash mismatch: expected prefix %s, got %s", expected_prefix, actual[:32])
        return False
    return True


class SpamModelV2:
    def __init__(self, path: Path = DEFAULT_MODEL, verify_hash: bool = True):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Spam model not found: {path}")

        meta = self._load_metadata(DEFAULT_META)
        expected_prefix = meta.get("model_sha256_prefix", "")

        if verify_hash and expected_prefix:
            if not _verify_model_hash(path, expected_prefix):
                raise RuntimeError(
                    f"Model integrity check failed for {path}. "
                    f"Expected prefix: {expected_prefix}. Refusing to load."
                )
            logger.info("Model hash verified: %s", expected_prefix)

        self.pipe = joblib.load(path)
        self.tfidf = self.pipe.named_steps["tfidf"]
        self.clf = self.pipe.named_steps["clf"]
        self.margin = TRIAGE_MARGIN
        self.path = path
        self.metadata = meta

    def _load_metadata(self, meta_path):
        try:
            return json.loads(Path(meta_path).read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Metadata not found at %s, using defaults", meta_path)
            return {"model_name": "spam_v2", "model_version": "2.0"}

    def score(self, text: str) -> float:
        return float(self.clf.decision_function(self.tfidf.transform([text]))[0])

    def classify(self, text: str):
        """Returns (label, margin). label in {'spam','ham','needs_human_triage'}."""
        m = self.score(text)
        if m > self.margin:
            return "spam", m
        if m < -self.margin:
            return "ham", m
        return "needs_human_triage", m

    def is_spam(self, text: str) -> bool:
        """Hard spam check (used where a boolean is required)."""
        return self.classify(text)[0] == "spam"

    def hard_label(self, text: str) -> str:
        """Decoded hard label without triage: 1->spam, 0->ham."""
        raw = str(self.pipe.predict([text])[0])
        return "spam" if raw == "1" else "ham"

    def version(self) -> str:
        return str(self.metadata.get("model_version", "2.0"))

    def trace(self) -> dict:
        """Human/machine-readable provenance for the loaded model."""
        return {
            "model": self.metadata.get("model_name"),
            "version": self.version(),
            "artifact": str(self.path),
            "dataset": self.metadata.get("dataset"),
            "metrics": self.metadata.get("metrics"),
            "trained_by": self.metadata.get("trained_by"),
            "trained_at": self.metadata.get("trained_at"),
            "sha256": self.metadata.get("model_sha256_prefix"),
        }