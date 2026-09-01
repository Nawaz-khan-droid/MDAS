# MDAS MVP Readiness Report

## Architecture

```
MDAS MVP
    │
    ├── Web UI (Jinja2 + HTMX + CSS)
    │   ├── /          Landing Page
    │   ├── /app       Analyzer Workspace
    │   └── /api-docs  API Documentation
    │
    ├── REST API
    │   └── POST /api/v1/analyze
    │
    └── AnalysisService
        ├── spaCy (en_core_web_sm, excl NER)
        ├── Lightweight Sentiment (VADER lexicon)
        ├── Spam Classifier (TF-IDF + LinearSVC)
        └── Voice Analysis (dependency rules)
```

## Active Features

### P0 — Clause-Level Voice Analysis
- **Status**: Production-ready
- **Accuracy**: 84.6% overall (atomic: ~100%, multi-clause: ~72%)
- **Output**: Active / Passive / Linking / Mixed / Uncertain
- **Evidence**: Subject, Verb, Auxiliary, Object, Agent, Copula, Complement
- **Method**: spaCy dependency parsing + rule-based classification

### P1 — Radar Signals
- **Status**: Production-ready
- **Signals**: Sentiment, Toxicity, Sarcasm (experimental), Urgency, Churn Risk
- **Method**: VADER sentiment + lexical baseline rules
- **Range**: 0.0 — 1.0

### P1 — ABSA (Aspect-Based Sentiment)
- **Status**: Production-ready
- **Method**: Dependency patterns + VADER polarity
- **Output**: Aspect-descriptor pairs with sentiment label

### P1 — Spam Detection
- **Status**: Production-ready
- **Model**: TF-IDF + LinearSVC (~206 KB)
- **Output**: ham / spam

### P1 — Language & Statistics
- **Status**: Production-ready
- **Detection**: langdetect
- **Stats**: Words, sentences, tokens, paragraphs, reading time

## Intentionally Removed / Archived

| Feature | Status | Reason |
|---------|--------|--------|
| Intent Classification | Archived | Requires PyTorch (~300 MB+) |
| MiniLM / SentenceTransformers | Archived | Training-only dependency |
| Topic / Category | Archived | Not needed for MVP |
| NLTK VADER | Replaced | Replaced with lightweight lexicon loader (saves 107 MB) |

## Dependency Inventory

### Production Dependencies
```
numpy, pandas, scikit-learn, joblib
spacy (en_core_web_sm)
fastapi, uvicorn
langdetect
jinja2-fragments
```

### Training Dependencies (optional)
```
sentence-transformers
streamlit
plotly
```

## Memory Measurements

| Metric | Value |
|--------|-------|
| Startup RSS | 246 MB |
| Post-load RSS | 386 MB |
| Peak at 1K input | 456 MB |
| Peak at 5K input | 474 MB |
| 512 MB headroom | 38 MB |
| spaCy model load | 265 MB |
| Lightweight sentiment | 3.3 MB |

## Latency Measurements

| Input Size | Latency (p50) | Clauses |
|------------|---------------|---------|
| 500 chars | 16 ms | 25 |
| 1000 chars | 26 ms | 52 |
| 2000 chars | 47 ms | 103 |
| 3000 chars | 78 ms | 154 |
| 4000 chars | 111 ms | 207 |
| 5000 chars | 110 ms | 259 |

## API Limits

- **Max input**: 5,000 characters (single source of truth: `MAX_TEXT_LENGTH`)
- **Empty text**: 400 Bad Request
- **Oversized**: 413 Payload Too Large
- **Unsupported language**: 400 with language details

## Deployment

### Render Free Tier Configuration
```yaml
services:
  - type: web
    name: mdas
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt && python -m spacy download en_core_web_sm
    startCommand: uvicorn mdas.api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: PYTHONPATH
        value: "src"
```

### Health Check
```
GET /health → {"status": "online", "models_loaded": true}
```

## Known Limitations

1. **Memory**: 38 MB headroom at 5K input. Concurrent requests may risk OOM.
2. **Voice Accuracy**: 84.6% overall. Multi-clause tiers at ~72%.
3. **Sarcasm**: Experimental only. No validated model.
4. **Toxicity**: Keyword-based only. Not ML-powered.
5. **English only**: No multi-language support.

## Hard Constraints

- 512 MB Render Free Tier memory limit
- 5,000 character input limit
- spaCy en_core_web_sm required
- No PyTorch in production
- No sentence-transformers in production

## Soft Constraints

- Single concurrent request recommended
- 500 ms latency budget at 5K input

## Repository Hygiene

- [x] No hardcoded developer paths
- [x] No __pycache__ in repo
- [x] No .venv in repo
- [x] Comprehensive .gitignore
- [x] Single configuration source (constants.py)
- [x] No conflicting limits (5K everywhere)
- [x] Training deps separated from production

## Remaining Risks

1. **Render OOM**: 38 MB headroom is tight. First optimization: pre-load VADER lexicon at startup instead of lazy load.
2. **Voice accuracy on complex text**: 72% on multi-clause. Needs held-out evaluation set.
3. **Spam false positives**: Not thoroughly evaluated for production edge cases.
4. **No render.yaml tested**: Deployment not verified end-to-end on Render.

## GO/NO-GO

**Conditional GO** — Safe for single-user demo deployment on Render Free Tier. Not safe for production traffic without memory optimization or upgrading to paid tier.
