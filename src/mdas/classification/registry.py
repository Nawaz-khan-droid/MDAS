import json
from pathlib import Path
from mdas.classification.model import TextClassifier
from mdas.core.errors import ModelUnavailableError
TASKS=("spam","sentiment","intent","category","moderation","document_type","sarcasm")
class ModelRegistry:
    def __init__(self, model_dir):
        self.model_dir=Path(model_dir); self.models={}
        for task in TASKS:
            a=self.model_dir/f"{task}.joblib"; m=self.model_dir/f"{task}.json"
            if a.exists() and m.exists(): self.models[task]=TextClassifier(a,json.loads(m.read_text(encoding="utf-8")))
    def has(self,task): return task in self.models
    def list_tasks(self): return list(self.models.keys())
    def predict(self,task,text):
        if task not in self.models: raise ModelUnavailableError(f"No trained '{task}' model in {self.model_dir}")
        return self.models[task].predict(text)
