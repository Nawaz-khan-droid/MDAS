import argparse, json
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from mdas.training.datasets import load_task_data
DOMAINS={"spam":"SMS spam/ham","sentiment":"Twitter US airline sentiment","intent":"customer support intent","category":"consumer complaint product/category","moderation":"user-supplied content moderation taxonomy","document_type":"user-supplied document type taxonomy"}
def pipeline():
    return Pipeline([("tfidf",TfidfVectorizer(lowercase=True,strip_accents="unicode",ngram_range=(1,2),min_df=2,max_features=30000,sublinear_tf=True)),("classifier",LogisticRegression(max_iter=1500,class_weight="balanced"))])
def train_one(task,data_dir,out_dir,seed=42):
    df=load_task_data(data_dir,task); xtr,xte,ytr,yte=train_test_split(df.text,df.label,test_size=.2,random_state=seed,stratify=df.label)
    model=pipeline(); model.fit(xtr,ytr); pred=model.predict(xte); f1=f1_score(yte,pred,average="macro")
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True); joblib.dump(model,out_dir/f"{task}.joblib")
    meta={"task":task,"model_name":"TF-IDF + LogisticRegression","domain":DOMAINS[task],"labels":sorted(map(str,model.classes_)),"train_rows":len(xtr),"test_rows":len(xte),"macro_f1":round(float(f1),5),"seed":seed,"classification_report":classification_report(yte,pred,output_dict=True,zero_division=0)}
    (out_dir/f"{task}.json").write_text(json.dumps(meta,indent=2),encoding="utf-8"); print(f"[{task}] rows={len(df):,} macro_f1={f1:.4f}")
def main():
    p=argparse.ArgumentParser(); p.add_argument("--data-dir",default="data/raw",type=Path); p.add_argument("--output-dir",default="models",type=Path); p.add_argument("--task",choices=list(DOMAINS)+["all"],default="all"); a=p.parse_args()
    for t in DOMAINS if a.task=="all" else [a.task]: train_one(t,a.data_dir,a.output_dir)
if __name__=="__main__": main()
