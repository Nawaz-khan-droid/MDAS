import spacy
from mdas.core.errors import BackendUnavailableError

class SpacyBackend:
    name = "spaCy"

    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            # PHASE 1: Load spaCy strictly for Voice/Dependency parsing. 
            # Exclude ONLY NER. Lemmatizer is REQUIRED for Voice rules (e.g. checking if verb lemma is "be").
            self.nlp = spacy.load(model_name, exclude=["ner"])
            
            # Inject lightweight domain EntityRuler before the parser
            ruler = self.nlp.add_pipe("entity_ruler", before="parser")
            patterns = [
                {"label": "ORG", "pattern": [{"LOWER": "dmart"}]},
                {"label": "ORG", "pattern": [{"LOWER": "flipkart"}]},
                {"label": "ORG", "pattern": [{"LOWER": "myntra"}]},
                {"label": "ORG", "pattern": [{"LOWER": "amazon"}]},
                {"label": "ORG", "pattern": [{"LOWER": "adidas"}]},
                {"label": "ORG", "pattern": [{"LOWER": "nike"}]},
                {"label": "ORG", "pattern": [{"LOWER": "puma"}]},
                {"label": "ORG", "pattern": [{"LOWER": "reliance"}]},
                {"label": "ORG", "pattern": [{"LOWER": "microsoft"}]},
                {"label": "ORG", "pattern": [{"LOWER": "apple"}]},
                {"label": "ORG", "pattern": [{"LOWER": "google"}]},
                {"label": "PRODUCT", "pattern": [{"LOWER": "shoes"}]},
                {"label": "PRODUCT", "pattern": [{"LOWER": "laptop"}]},
                {"label": "PRODUCT", "pattern": [{"LOWER": "mango"}]},
                {"label": "LOCATION", "pattern": [{"LOWER": "mumbai"}]},
                {"label": "LOCATION", "pattern": [{"LOWER": "delhi"}]},
                {"label": "LOCATION", "pattern": [{"LOWER": "bangalore"}]},
                {"label": "DATE", "pattern": [{"LOWER": "today"}]},
                {"label": "DATE", "pattern": [{"LOWER": "tomorrow"}]},
                {"label": "DATE", "pattern": [{"LOWER": "yesterday"}]}
            ]
            ruler.add_patterns(patterns)
            
        except OSError as exc:
            raise BackendUnavailableError(
                f"spaCy model '{model_name}' is not installed. "
                f"Run: python -m spacy download {model_name}"
            ) from exc

    def analyze(self, text: str):
        return self.nlp(text)

    def pipe(self, texts: list[str]):
        return list(self.nlp.pipe(texts))
