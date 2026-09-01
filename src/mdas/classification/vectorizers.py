from sklearn.base import BaseEstimator, TransformerMixin

class MiniLMVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        if isinstance(X, str):
            X = [X]
        return self._model.encode(list(X), show_progress_bar=False)
