from mdas.core.errors import BackendUnavailableError

class StanzaBackend:
    """Optional backend using Stanza directly, not NLP Suite private modules."""
    name = "Stanza"

    def __init__(self):
        try:
            import stanza
        except ImportError as exc:
            raise BackendUnavailableError(
                "Install Stanza with: pip install -e '.[stanza]'"
            ) from exc
        try:
            self.nlp = stanza.Pipeline(
                "en", processors="tokenize,pos,lemma,depparse,ner", use_gpu=False
            )
        except Exception as exc:
            raise BackendUnavailableError(
                "Could not initialize Stanza English models. Download the English model first."
            ) from exc

    def analyze(self, text: str):
        return self.nlp(text)

    def pipe(self, texts: list[str]):
        return [self.nlp(t) for t in texts]
