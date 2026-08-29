from pathlib import Path
import joblib
from mdas.core.errors import ModelUnavailableError
from mdas.core.types import ClassificationResult

class TextClassifier:
    def __init__(self, artifact_path: Path, metadata: dict):
        if not artifact_path.exists(): raise ModelUnavailableError(f"Missing model artifact: {artifact_path}")
        self.pipeline=joblib.load(artifact_path); self.metadata=metadata
    def predict(self, text):
        label=str(self.pipeline.predict([text])[0]); confidence=None; alternatives=[]
        if hasattr(self.pipeline,"predict_proba"):
            ranked=sorted(zip(self.pipeline.classes_,self.pipeline.predict_proba([text])[0]),key=lambda x:x[1],reverse=True)
            confidence=float(ranked[0][1]); alternatives=[{"label":str(x),"confidence":round(float(p),4)} for x,p in ranked[:3]]
        return ClassificationResult(label,round(confidence,4) if confidence is not None else None,"ok",self.metadata.get("model_name"),self.metadata.get("domain"),alternatives)
