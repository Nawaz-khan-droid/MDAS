from pathlib import Path
from mdas.analysis.language import identify_english
from mdas.analysis.linguistics import analyze_linguistics
from mdas.analysis.signals import build_signals,sentiment_signal_from_label
from mdas.analysis.statistics import analyze_statistics
from mdas.classification.registry import ModelRegistry
from mdas.core.config import MDASConfig
from mdas.core.errors import InputValidationError
from mdas.core.types import AnalysisResult
from mdas.nlp.spacy_backend import SpacyBackend

class MDASAnalyzer:
    """Stable application service. Future UIs should call this, not internals."""
    def __init__(self,backend,registry=None,config=None): self.backend=backend; self.registry=registry; self.config=config or MDASConfig()
    @classmethod
    def from_directory(cls,model_dir="models",backend="spacy"):
        config=MDASConfig(model_dir=Path(model_dir))
        if backend=="spacy": nlp=SpacyBackend()
        elif backend=="stanza":
            from mdas.nlp.stanza_backend import StanzaBackend
            nlp=StanzaBackend()
        else: raise ValueError(f"Unsupported backend: {backend}")
        return cls(nlp,ModelRegistry(config.model_dir),config)
    def analyze(self,text):
        self._validate(text); doc=self.backend.analyze(text)
        stats=analyze_statistics(doc); ling=analyze_linguistics(doc,self.config.include_token_details)
        classification={}; warnings=[]
        for task in ("spam","sentiment","intent","category","moderation","document_type"):
            if not self.registry or not self.registry.has(task):
                classification[task]={"label":None,"confidence":None,"status":"model_unavailable"}; warnings.append(f"No trained {task} model is available; classification omitted.")
            else:
                r=self.registry.predict(task,text); classification[task]={"label":r.label,"confidence":r.confidence,"status":r.status,"model":r.model,"domain":r.domain,"alternatives":r.alternatives}
        sent=classification["sentiment"]["label"]; signals=build_signals(text,sent)
        radar={"sentiment":sentiment_signal_from_label(sent),"urgency":signals["urgency"]["score"],"churn_risk":signals["churn_risk"]["score"],"toxicity":signals["toxicity"]["score"],"sarcasm":signals["sarcasm"]["score"]}
        return AnalysisResult(meta={"language":identify_english(text),"backend":self.backend.name,"input_characters":len(text),"max_characters":self.config.max_characters},statistics=stats,linguistics=ling,classification=classification,radar=radar,signals=signals,warnings=warnings)
    def _validate(self,text):
        if not isinstance(text,str): raise InputValidationError("text must be a string")
        if not text.strip(): raise InputValidationError("text must not be empty")
        if len(text)>self.config.max_characters: raise InputValidationError(f"text exceeds {self.config.max_characters:,} characters")
