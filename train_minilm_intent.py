import pandas as pd
import joblib
import json
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from mdas.classification.vectorizers import MiniLMVectorizer

def train_minilm_intent():
    print("Training MiniLM fallback model for intent...")
    df = pd.read_csv("data/raw/intent.csv").dropna()
    
    if len(df) > 5000:
        df = df.sample(5000, random_state=42)
        
    X = df["text"].tolist()
    y = df["label"].tolist()

    pipeline = Pipeline([
        ("vectorizer", MiniLMVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])
    
    pipeline.fit(X, y)
    
    joblib.dump(pipeline, "models/minilm_intent.joblib")
    
    metadata = {
        "model_name": "minilm_intent",
        "version": "v1.1",
        "description": "MiniLM fallback for intent",
        "training_samples": len(df)
    }
    with open("models/minilm_intent.json", "w") as f:
        json.dump(metadata, f)
        
    print("Saved minilm_intent.joblib!")

if __name__ == "__main__":
    train_minilm_intent()
