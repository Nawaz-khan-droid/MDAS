from pathlib import Path
import pandas as pd
REQUIRED={"spam":("spam.csv","text","label"),"sentiment":("sentiment.csv","text","label"),"intent":("intent.csv","text","label"),"category":("category.csv","text","label"),"moderation":("moderation.csv","text","label"),"document_type":("document_type.csv","text","label")}
def load_task_data(data_dir,task):
    filename,tc,lc=REQUIRED[task]; path=Path(data_dir)/filename
    if not path.exists(): raise FileNotFoundError(f"Missing {task} dataset: {path}")
    df=pd.read_csv(path)
    if tc not in df or lc not in df: raise ValueError(f"{path} requires columns {tc!r} and {lc!r}")
    df=df[[tc,lc]].rename(columns={tc:"text",lc:"label"}).dropna().drop_duplicates()
    df["text"]=df.text.astype(str); df["label"]=df.label.astype(str)
    counts=df.label.value_counts(); df=df[df.label.isin(counts[counts>=2].index)].reset_index(drop=True)
    if df.label.nunique()<2: raise ValueError(f"{task} needs at least two classes")
    return df
