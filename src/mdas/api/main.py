import os
import uuid
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel
from mdas.api.schemas import AnalysisRequest, AnalysisResponse, UnsupportedLanguageResponse
from mdas.application.analysis_service import AnalysisService

app = FastAPI(
    title="MDAS Keyless API",
    description="Multi-Dimensional Text Analysis System - Local NLP Inference API",
    version="0.1.0"
)

# Set up templates using jinja2-fragments
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Blocks(directory=TEMPLATE_DIR)

# Initialize Analyzer on Startup
analyzer = None

@app.on_event("startup")
def load_models():
    global analyzer
    try:
        analyzer = AnalysisService(model_dir="models")
        print("MDAS AnalysisService loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not initialize AnalysisService on startup: {e}")

@app.get("/health")
def health_check():
    return {"status": "online", "models_loaded": analyzer is not None}

# ==========================================
# REST API V1
# ==========================================

@app.post("/api/v1/analyze", response_model=AnalysisResponse)
def analyze_text_api(request: AnalysisRequest):
    if not analyzer:
        raise HTTPException(status_code=503, detail="MDAS Engine is not loaded.")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    try:
        result = analyzer.analyze(request.text, analysis_id=str(uuid.uuid4()))
        if isinstance(result, UnsupportedLanguageResponse):
            raise HTTPException(status_code=400, detail=result.dict())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# HTMX WEB UI
# ==========================================

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.post("/ui/analyze", response_class=HTMLResponse)
def analyze_text_ui(request: Request, text: str = Form(...)):
    if not analyzer:
        return templates.TemplateResponse(request, "index.html", {"request": request, "error": "MDAS Engine is not loaded."}, block_name="result")
    
    if not text.strip():
        return templates.TemplateResponse(request, "index.html", {"request": request, "error": "Text cannot be empty."}, block_name="result")
        
    try:
        result = analyzer.analyze(text, analysis_id=str(uuid.uuid4()))
        if isinstance(result, UnsupportedLanguageResponse):
            ctx = result.language.dict()
            ctx["request"] = request
            ctx["status"] = "unsupported_language"
            return templates.TemplateResponse(request, "index.html", ctx, block_name="result")
            
        ctx = result.dict()
        ctx["request"] = request
        return templates.TemplateResponse(request, "index.html", ctx, block_name="result")
    except Exception as e:
        return templates.TemplateResponse(request, "index.html", {"request": request, "error": str(e)}, block_name="result")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mdas.api.main:app", host="0.0.0.0", port=8002, reload=True)
