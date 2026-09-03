import os
import time
import uuid
import logging
import concurrent.futures
from pathlib import Path
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel
from mdas.api.schemas import AnalysisRequest, AnalysisResponse, UnsupportedLanguageResponse

# ==========================================
# LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mdas")

# ==========================================
# TIMEOUT
# ==========================================
ANALYSIS_TIMEOUT_SECONDS = int(os.environ.get("MDAS_TIMEOUT", "30"))

# ==========================================
# ENGINE VERSION (feature flag)
# ==========================================
USE_V2 = os.environ.get("MDAS_V2", "false").lower() in {"1", "true", "yes"}
logger.info("Engine version: V2=%s (MDAS_V2 env: %s)", USE_V2, os.environ.get("MDAS_V2", "unset"))

# Initialize app state
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        if USE_V2:
            from mdas.v2 import V2AnalysisService
            app.state.analyzer = V2AnalysisService()
            app.state.engine_version = "v2"
            logger.info("MDAS V2 AnalysisService loaded successfully.")
        else:
            from mdas.application.analysis_service import AnalysisService
            app.state.analyzer = AnalysisService(model_dir="models", allowed_tasks=["spam"])
            app.state.engine_version = "v1"
            logger.info("MDAS V1 AnalysisService loaded successfully.")
    except Exception as e:
        logger.exception("Failed to initialize AnalysisService on startup: %s", e)
        app.state.analyzer = None
        app.state.engine_version = "failed"
        
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

# ==========================================
# RATE LIMITING (sliding window per IP)
# ==========================================
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 30  # per window per IP
_rate_limit_store: dict[str, list[float]] = defaultdict(list)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        cutoff = now - RATE_LIMIT_WINDOW
        # Prune old entries
        _rate_limit_store[client_ip] = [t for t in _rate_limit_store[client_ip] if t > cutoff]
        if len(_rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
            retry_after = int(_rate_limit_store[client_ip][0] + RATE_LIMIT_WINDOW - now) + 1
            return JSONResponse(
                status_code=429,
                content={"status": "error", "error": {"code": "RATE_LIMITED", "message": "Too many requests. Try again shortly."}},
                headers={"Retry-After": str(retry_after)},
            )
        _rate_limit_store[client_ip].append(now)
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)

# ==========================================
# SECURITY HEADERS (HSTS, etc.)
# ==========================================
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

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
TEMPLATE_DIR = str(Path(__file__).resolve().parent.parent / "templates")
templates = Jinja2Blocks(directory=TEMPLATE_DIR)

@app.get("/api/v1/mdas/health")
def health_check():
    is_ready = hasattr(app.state, "analyzer") and app.state.analyzer is not None
    version = getattr(app.state, "engine_version", "unknown")
    return {"status": "online", "engine": version, "models_loaded": is_ready}

# ==========================================
# REST API V1
# ==========================================

@app.post("/api/v1/mdas/analyze", response_model=AnalysisResponse)
def analyze_text_api(request: AnalysisRequest, req: Request):
    if not hasattr(req.app.state, "analyzer") or not req.app.state.analyzer:
        return JSONResponse(status_code=503, content={"status": "error", "error": {"code": "SERVICE_UNAVAILABLE", "message": "MDAS Engine is not loaded or initializing."}})
    
    if not request.text.strip():
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "BAD_REQUEST", "message": "Text cannot be empty."}})
        
    analysis_id = str(uuid.uuid4())
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(req.app.state.analyzer.analyze, request.text, analysis_id)
            result = future.result(timeout=ANALYSIS_TIMEOUT_SECONDS)
        if isinstance(result, UnsupportedLanguageResponse):
            return JSONResponse(status_code=400, content=result.dict())
        return result
    except concurrent.futures.TimeoutError:
        logger.error("Analysis timed out after %ds for request %s", ANALYSIS_TIMEOUT_SECONDS, analysis_id)
        return JSONResponse(status_code=504, content={"status": "error", "error": {"code": "TIMEOUT", "message": f"Analysis timed out after {ANALYSIS_TIMEOUT_SECONDS}s."}})
    except ValueError as ve:
        if "exceeds maximum allowed" in str(ve):
            return JSONResponse(status_code=413, content={"status": "error", "error": {"code": "PAYLOAD_TOO_LARGE", "message": str(ve)}})
        return JSONResponse(status_code=400, content={"status": "error", "error": {"code": "VALIDATION_FAILED", "message": str(ve)}})
    except Exception as e:
        logger.exception("Analysis failed for request %s", analysis_id)
        return JSONResponse(status_code=500, content={"status": "error", "error": {"code": "ANALYSIS_FAILED", "message": "The text could not be analyzed."}})



# ==========================================
# HTMX WEB UI SURFACES
# ==========================================

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/app", response_class=HTMLResponse)
def analysis_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request, "max_text_length": MAX_TEXT_LENGTH})
    
@app.get("/api-docs", response_class=HTMLResponse)
def custom_docs(request: Request):
    return templates.TemplateResponse("docs.html", {"request": request})

@app.post("/ui/analyze", response_class=HTMLResponse)
def analyze_text_ui(request: Request, text: str = Form(...)):
    if not hasattr(request.app.state, "analyzer") or not request.app.state.analyzer:
        return templates.TemplateResponse("app.html", {"request": request, "error": "MDAS Engine is not loaded.", "text": text}, block_name="result")
    
    if not text.strip():
        return templates.TemplateResponse("app.html", {"request": request, "error": "Text cannot be empty.", "text": text}, block_name="result")
        
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(request.app.state.analyzer.analyze, text, str(uuid.uuid4()))
            result = future.result(timeout=ANALYSIS_TIMEOUT_SECONDS)
        if isinstance(result, UnsupportedLanguageResponse):
            ctx = result.dict()
            ctx["request"] = request
            ctx["status"] = "unsupported_language"
            ctx["text"] = text
            return templates.TemplateResponse("app.html", ctx, block_name="result")
            
        ctx = result.dict()
        ctx["request"] = request
        ctx["text"] = text
        return templates.TemplateResponse("app.html", ctx, block_name="result")
    except concurrent.futures.TimeoutError:
        logger.error("UI analysis timed out after %ds", ANALYSIS_TIMEOUT_SECONDS)
        return templates.TemplateResponse("app.html", {"request": request, "error": f"Analysis timed out after {ANALYSIS_TIMEOUT_SECONDS}s.", "text": text}, block_name="result")
    except ValueError as ve:
        return templates.TemplateResponse("app.html", {"request": request, "error": str(ve), "text": text}, block_name="result")
    except Exception as e:
        logger.exception("UI analysis failed")
        return templates.TemplateResponse("app.html", {"request": request, "error": "The text could not be analyzed.", "text": text}, block_name="result")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mdas.api.main:app", host="0.0.0.0", port=8002, reload=True)
