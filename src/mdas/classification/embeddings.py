from sklearn.base import BaseEstimator, TransformerMixin
from sentence_transformers import SentenceTransformer
import numpy as np

class DenseTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        
    def __getstate__(self):
        state = self.__dict__.copy()
        state["_model"] = None # Don't pickle the 90mb model
        return state
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        # Handle single string or list of strings
        if isinstance(X, str):
            X = [X]
        # X can be a pandas Series, list, or numpy array
        if hasattr(X, "tolist"):
            X = X.tolist()
        return self._model.encode(X, show_progress_bar=False)
