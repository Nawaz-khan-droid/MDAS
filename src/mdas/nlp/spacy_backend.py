import spacy
from mdas.core.errors import BackendUnavailableError

class SpacyBackend:
    name = "spaCy"

    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError as exc:
            raise BackendUnavailableError(
                f"spaCy model '{model_name}' is not installed. "
                f"Run: python -m spacy download {model_name}"
            ) from exc

    def analyze(self, text: str):
        return self.nlp(text)

    def pipe(self, texts: list[str]):
        return list(self.nlp.pipe(texts))
