import os
import uuid
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel
from mdas.api.schemas import AnalysisRequest, AnalysisResponse, UnsupportedLanguageResponse
from mdas.application.analysis_service import AnalysisService

# Initialize app state
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        app.state.analyzer = AnalysisService(model_dir="models", allowed_tasks=["spam"])
        print("MDAS AnalysisService loaded successfully in lifespan.")
    except Exception as e:
        print(f"Warning: Could not initialize AnalysisService on startup: {e}")
        app.state.analyzer = None
        
    yield
    # Shutdown (cleanup if needed)
    app.state.analyzer = None

app = FastAPI(
    title="MDAS Keyless API",
    description="Multi-Dimensional Text Analysis System - Local NLP Inference API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

from fastapi.exceptions import RequestValidationError
from mdas.core.constants import MAX_TEXT_LENGTH

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Check if this is a max_length validation error
    for error in errors:
        if error.get("type") == "string_too_long":
            return JSONResponse(
                status_code=413,
                content={"status": "error", "error": {"code": "PAYLOAD_TOO_LARGE", "message": f"Text exceeds maximum allowed length of {MAX_TEXT_LENGTH} characters."}}
            )
    msg = errors[0]["msg"] if errors else "Invalid request data"
    return JSONResponse(
        status_code=400,
        content={"status": "error", "error": {"code": "VALIDATION_FAILED", "message": msg}}
    )

# Set up templates using jinja2-fragments
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Blocks(directory=TEMPLATE_DIR)

@app.get("/api/v1/mdas/health")
def health_check():
    is_ready = hasattr(app.state, "analyzer") and app.state.analyzer is not None
    return {"status": "online", "models_loaded": is_ready}

# ==========================================
# REST API V1
# ==========================================

@app.post("/api/v1/mdas/analyze", response_model=AnalysisResponse)
def analyze_text_api(request: AnalysisRequest, req: Request):
    if not hasattr(req.app.state, "analyzer") or not req.app.state.analyzer:
        return JSONResponse(status_code=503, content={"status": "error", "error": {"code": "SERVICE_UNAVAILABLE", "message": "MDAS Engine is not loaded or initializing."}})
    
    if not request.text.strip():
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "BAD_REQUEST", "message": "Text cannot be empty."}})
        
    try:
        result = req.app.state.analyzer.analyze(request.text, analysis_id=str(uuid.uuid4()))
        if isinstance(result, UnsupportedLanguageResponse):
            return JSONResponse(status_code=400, content=result.dict())
        return result
    except ValueError as ve:
        if "exceeds maximum allowed" in str(ve):
            return JSONResponse(status_code=413, content={"status": "error", "error": {"code": "PAYLOAD_TOO_LARGE", "message": str(ve)}})
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "VALIDATION_FAILED", "message": str(ve)}})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "error": {"code": "ANALYSIS_FAILED", "message": "The text could not be analyzed."}})



# ==========================================
# HTMX WEB UI SURFACES
# ==========================================

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse(request, "landing.html", {"request": request})

@app.get("/app", response_class=HTMLResponse)
def analysis_app(request: Request):
    return templates.TemplateResponse(request, "app.html", {"request": request, "max_text_length": MAX_TEXT_LENGTH})
    
@app.get("/api-docs", response_class=HTMLResponse)
def custom_docs(request: Request):
    return templates.TemplateResponse(request, "docs.html", {"request": request})

@app.post("/ui/analyze", response_class=HTMLResponse)
def analyze_text_ui(request: Request, text: str = Form(...)):
    if not hasattr(request.app.state, "analyzer") or not request.app.state.analyzer:
        return templates.TemplateResponse(request, "app.html", {"request": request, "error": "MDAS Engine is not loaded.", "text": text}, block_name="result")
    
    if not text.strip():
        return templates.TemplateResponse(request, "app.html", {"request": request, "error": "Text cannot be empty.", "text": text}, block_name="result")
        
    try:
        result = request.app.state.analyzer.analyze(text, analysis_id=str(uuid.uuid4()))
        if isinstance(result, UnsupportedLanguageResponse):
            ctx = result.dict()
            ctx["request"] = request
            ctx["status"] = "unsupported_language"
            ctx["text"] = text
            return templates.TemplateResponse(request, "app.html", ctx, block_name="result")
            
        ctx = result.dict()
        ctx["request"] = request
        ctx["text"] = text
        return templates.TemplateResponse(request, "app.html", ctx, block_name="result")
    except ValueError as ve:
        # Pass the error message to the template
        return templates.TemplateResponse(request, "app.html", {"request": request, "error": str(ve), "text": text}, block_name="result")
    except Exception as e:
        traceback.print_exc()
        return templates.TemplateResponse(request, "app.html", {"request": request, "error": "The text could not be analyzed.", "text": text}, block_name="result")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mdas.api.main:app", host="0.0.0.0", port=8002, reload=True)
