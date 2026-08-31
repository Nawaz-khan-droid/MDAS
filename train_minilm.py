import pandas as pd
import joblib
import json
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from mdas.classification.vectorizers import MiniLMVectorizer

def train_model(task_name):
    print(f"Training MiniLM model for {task_name}...")
    df = pd.read_csv(f"data/raw/{task_name}.csv").dropna()
    
    # Subsample if dataset is too large to speed up MVP training
    if len(df) > 5000:
        df = df.sample(5000, random_state=42)
        
    X = df["text"].tolist()
    y = df["label"].tolist()

    pipeline = Pipeline([
        ("vectorizer", MiniLMVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])
    
    pipeline.fit(X, y)
    
    # Save model
    joblib.dump(pipeline, f"models/{task_name}.joblib")
    
    # Save metadata
    metadata = {
        "model_name": f"minilm_lr_{task_name}",
        "version": "v1.1",
        "description": f"{task_name} classification using MiniLM vectors",
        "training_samples": len(df)
    }
    with open(f"models/{task_name}.json", "w") as f:
        json.dump(metadata, f)
        
    print(f"Saved {task_name}.joblib!")

if __name__ == "__main__":
    train_model("intent")
    train_model("spam")
