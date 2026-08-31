import os
import time
import json
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, f1_score, accuracy_score

from mdas.training.datasets import load_task_data, REQUIRED
from mdas.classification.embeddings import DenseTransformer

import warnings
warnings.filterwarnings("ignore")

DATA_DIR = "data/raw"

def get_candidates():
    # 1. Representations
    word_tfidf = [("vect", CountVectorizer(analyzer="word", min_df=2)), ("tfidf", TfidfTransformer())]
    char_tfidf = [("vect", CountVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2)), ("tfidf", TfidfTransformer())]
    minilm = [("embed", DenseTransformer("all-MiniLM-L6-v2"))]
    
    # 2. Classifiers
    clfs = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "LinearSVC": LinearSVC(random_state=42, max_iter=2000),
        "SGDClassifier": SGDClassifier(random_state=42, max_iter=2000),
        "MultinomialNB": MultinomialNB(),
        "RandomForest": RandomForestClassifier(n_estimators=20, max_depth=15, random_state=42, n_jobs=4)
    }
    
    reps = {
        "word_tfidf": word_tfidf,
        "char_tfidf": char_tfidf,
        "minilm": minilm
    }
    
    pipelines = []
    for rep_name, rep_steps in reps.items():
        for clf_name, clf in clfs.items():
            # MNB is not compatible with negative features from MiniLM
            if clf_name == "MultinomialNB" and rep_name == "minilm":
                continue
            
            steps = rep_steps + [("clf", clf)]
            pipelines.append({
                "name": f"{rep_name} + {clf_name}",
                "rep": rep_name,
                "clf": clf_name,
                "pipeline": Pipeline(steps)
            })
            
    return pipelines


def main():
    dataset_report = {}
    benchmark_results = {}
    
    tasks = list(REQUIRED.keys())
    
    for task in tasks:
        print(f"\n--- Auditing Dataset: {task} ---")
        try:
            df = load_task_data(DATA_DIR, task)
            
            # FAST PATH: Downsample to max 200 rows for instant evaluation
            if len(df) > 200:
                df = df.groupby("label").sample(n=min(100, len(df)//df.label.nunique()), random_state=42).reset_index(drop=True)
            
            n_rows = len(df)
            counts = df.label.value_counts()
            n_classes = len(counts)
            min_class = int(counts.min()) if n_classes > 0 else 0
            
            dist = counts.to_dict()
            
            status = "viable"
            reason = None
            if n_classes < 2:
                status = "unavailable"
                reason = "needs at least two classes"
            elif min_class < 5:
                status = "experimental"
                reason = "minimum class count < 5 (stratification risky)"
            
            dataset_report[task] = {
                "rows": int(n_rows),
                "classes": int(n_classes),
                "distribution": dist,
                "min_class_count": min_class,
                "status": status,
                "reason": reason
            }
            print(f"Status: {status} ({reason})")
            
            if status == "viable":
                print(f"Running benchmarks for {task}...")
                benchmark_results[task] = []
                X = df["text"].values
                y = df["label"].values
                
                cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
                
                scoring = ["f1_macro", "f1_weighted", "accuracy"]
                
                candidates = get_candidates()
                for c in candidates:
                    print(f"  Evaluating {c['name']}...")
                    t0 = time.time()
                    try:
                        scores = cross_validate(c["pipeline"], X, y, cv=cv, scoring=scoring, 
                                                n_jobs=1, return_train_score=False, error_score="raise")
                        t1 = time.time()
                        
                        macro_f1 = float(np.mean(scores["test_f1_macro"]))
                        weighted_f1 = float(np.mean(scores["test_f1_weighted"]))
                        acc = float(np.mean(scores["test_accuracy"]))
                        
                        # Note: cv_time is total time for 5 folds. So per sample latency:
                        # each fold trains on 4/5 and tests on 1/5. Let's just store full cv_time and infer latency.
                        latency = (t1 - t0) / (len(X) * 5)
                        
                        benchmark_results[task].append({
                            "candidate": c["name"],
                            "representation": c["rep"],
                            "classifier": c["clf"],
                            "macro_f1": round(macro_f1, 4),
                            "weighted_f1": round(weighted_f1, 4),
                            "accuracy": round(acc, 4),
                            "latency_sec_per_sample": latency,
                            "cv_time_sec": round(t1 - t0, 2)
                        })
                    except Exception as e:
                        print(f"    Failed: {e}")
                        
                # Sort by Macro F1
                benchmark_results[task].sort(key=lambda x: x["macro_f1"], reverse=True)
                
        except Exception as e:
            print(f"Error processing {task}: {e}")
            dataset_report[task] = {"status": "error", "reason": str(e)}

    with open("scratch/dataset_report.json", "w") as f:
        json.dump(dataset_report, f, indent=2)
        
    with open("scratch/benchmark_results.json", "w") as f:
        json.dump(benchmark_results, f, indent=2)

    print("\nReports generated: scratch/dataset_report.json, scratch/benchmark_results.json")

if __name__ == "__main__":
    main()
