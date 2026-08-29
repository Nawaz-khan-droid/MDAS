import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from mdas import MDASAnalyzer
from mdas.core.errors import InputValidationError
app=FastAPI(title="MDAS API",version="0.1.0")
_analyzer=None
class AnalyzeRequest(BaseModel): text:str=Field(min_length=1)
def get_analyzer():
    global _analyzer
    if _analyzer is None: _analyzer=MDASAnalyzer.from_directory(os.getenv("MDAS_MODEL_DIR","models"),os.getenv("MDAS_NLP_BACKEND","spacy"))
    return _analyzer
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/v1/analyze")
def analyze(request:AnalyzeRequest):
    try: return {"result":get_analyzer().analyze(request.text).to_dict()}
    except InputValidationError as e: raise HTTPException(422,str(e)) from e
    except Exception as e: raise HTTPException(500,str(e)) from e
