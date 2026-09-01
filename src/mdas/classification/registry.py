import json
from pathlib import Path
from mdas.classification.model import TextClassifier
from mdas.core.errors import ModelUnavailableError
from mdas.core.constants import PRODUCTION_TASKS

# Legacy tasks that require PyTorch/sentence-transformers (not used in production)
LEGACY_TASKS=("sentiment","intent","category","moderation","document_type","sarcasm","minilm_intent")
class ModelRegistry:
    def __init__(self, model_dir, allowed_tasks=None):
        self.model_dir=Path(model_dir); self.models={}
        # Default to production tasks only (no PyTorch dependencies)
        tasks_to_load = allowed_tasks if allowed_tasks is not None else PRODUCTION_TASKS
        for task in tasks_to_load:
            a=self.model_dir/f"{task}.joblib"; m=self.model_dir/f"{task}.json"
            if a.exists() and m.exists(): self.models[task]=TextClassifier(a,json.loads(m.read_text(encoding="utf-8")))
    def has(self,task): return task in self.models
    def list_tasks(self): return list(self.models.keys())
    def predict(self,task,text):
        if task not in self.models: raise ModelUnavailableError(f"No trained '{task}' model in {self.model_dir}")
        return self.models[task].predict(text)
