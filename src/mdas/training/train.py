import argparse, json
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from mdas.training.datasets import load_task_data
from mdas.classification.embeddings import DenseTransformer

from sklearn.calibration import CalibratedClassifierCV

DOMAINS={"spam":"SMS spam/ham","sentiment":"Twitter US airline sentiment","intent":"customer support intent","category":"consumer complaint product/category","moderation":"user-supplied content moderation taxonomy","document_type":"user-supplied document type taxonomy","sarcasm":"sarcasm detection"}

MODELS = {
    "LogisticRegression": lambda: LogisticRegression(max_iter=1500, class_weight="balanced"),
    "LinearSVC": lambda: CalibratedClassifierCV(LinearSVC(max_iter=1500, class_weight="balanced", dual=False), cv=3),
    "MultinomialNB": lambda: MultinomialNB()
}

def train_one(task,data_dir,out_dir,seed=42):
    df=load_task_data(data_dir,task); xtr,xte,ytr,yte=train_test_split(df.text,df.label,test_size=.2,random_state=seed,stratify=df.label)
    
    best_model = None
    best_f1 = -1
    best_name = ""
    best_pred = None
    
    print(f"\n--- Training [{task}] ---")
    for name, clf_func in MODELS.items():
        if name == "MultinomialNB":
            continue # NB doesn't handle negative values which dense embeddings have
            
        model = Pipeline([
            ("embeddings", DenseTransformer(model_name="all-MiniLM-L6-v2")),
            ("classifier", clf_func())
        ])
        model.fit(xtr, ytr)
        pred = model.predict(xte)
        f1 = f1_score(yte, pred, average="macro")
        print(f"  {name:20s} Macro F1: {f1:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_name = name
            best_pred = pred
            
    print(f"[{task}] SELECTED: {best_name} with F1={best_f1:.4f}")
    
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True); joblib.dump(best_model,out_dir/f"{task}.joblib")
    meta={"task":task,"model_name":f"SentenceTransformer + {best_name}","domain":DOMAINS[task],"labels":sorted(map(str,best_model.classes_)),"train_rows":len(xtr),"test_rows":len(xte),"macro_f1":round(float(best_f1),5),"seed":seed,"classification_report":classification_report(yte,best_pred,output_dict=True,zero_division=0)}
    (out_dir/f"{task}.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--data-dir",default="data/raw",type=Path); p.add_argument("--output-dir",default="models",type=Path); p.add_argument("--task",choices=list(DOMAINS)+["all"],default="all"); a=p.parse_args()
    for t in DOMAINS if a.task=="all" else [a.task]: train_one(t,a.data_dir,a.output_dir)
if __name__=="__main__": main()
