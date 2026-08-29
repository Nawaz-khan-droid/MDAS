from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mdas import MDASAnalyzer

app = FastAPI(
    title="MDAS Keyless API",
    description="Multi-Dimensional Text Analysis System - Local NLP Inference API",
    version="0.1.0"
)

# Initialize Analyzer on Startup
analyzer = None

@app.on_event("startup")
def load_models():
    global analyzer
    try:
        analyzer = MDASAnalyzer.from_directory("models")
    except Exception as e:
        print(f"Warning: Could not initialize models on startup: {e}")

class AnalysisRequest(BaseModel):
    text: str

@app.get("/health")
def health_check():
    return {"status": "online", "models_loaded": analyzer is not None}

@app.post("/api/analyze")
def analyze_text(request: AnalysisRequest):
    if not analyzer:
        raise HTTPException(status_code=503, detail="MDAS Engine is not loaded.")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    try:
        result = analyzer.analyze(request.text)
        return result.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mdas.api.main:app", host="0.0.0.0", port=8000, reload=True)
