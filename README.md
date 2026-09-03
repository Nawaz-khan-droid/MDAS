# MDAS

A text analysis API that runs on Render's free tier. No API keys, no paid services.

Clause-level voice analysis, aspect-based sentiment, spam detection, and radar signals (toxicity, urgency, churn, sarcasm). English only. 5,000 character limit. 512 MB of RAM to work with.

**Live:** `https://mdas-0x3n.onrender.com`

```bash
curl -X POST https://mdas-0x3n.onrender.com/api/v1/mdas/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "The customer opened the package."}'
```

## Getting it running locally

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
PYTHONPATH=src uvicorn mdas.api.main:app --reload
```

Tests: `PYTHONPATH=src pytest tests/`

## Two engines, same API

There's a V1 and a V2 engine. Set `MDAS_V2=true` to use V2. Same API, same endpoints. V2 swaps in better spam detection, ABSA patterns, and radar signals. Voice and sentiment are shared between both.

| | V1 | V2 |
|---|---|---|
| **Spam** | 123 training samples, 83.5% accuracy | 7,699 samples, 98.9% accuracy, triage for uncertain cases |
| **ABSA** | Adjective-on-noun patterns | Verb-predicate + compound nouns + negation-aware |
| **Radar** | Raw keyword counting | Negation-aware, phrase weighting, strong triggers |
| **Voice** | Dependency rules | Same |
| **Sentiment** | VADER | Same |

V2 builds on V1. It's not a rewrite, it's an improvement.

## What works and what doesn't

**Spam detection** is the strongest part of the system. 98.9% on held-out test data, 98.3% on a domain-specific benchmark. It uses margin-based triage, so when the model isn't sure it says "needs human review" instead of guessing wrong. Fewer false positives, uncertain cases get flagged.

**Voice analysis** is solid. It's rule-based on dependency parsing, which means it transfers to unseen text. 7/8 on independent test sentences. Structural rules generalize better than word lists.

**ABSA and radar** score well on the test sets I built them against (10/11 for ABSA, improved radar coverage). But on truly independent text they haven't seen during development, ABSA got 1/12 right. The radar improvements were built by adding words to catch specific test cases, which is coverage, not generalization. If you need these to work on arbitrary new phrasing, you'd want a trained model instead of hand-tuned patterns. The current versions are useful for known patterns but won't cover everything.

**Sarcasm** is heuristic-only, 0/1 in both versions. It's there for completeness, not reliability.

## API

### Health check

```
GET /api/v1/mdas/health
```

```json
{
  "status": "online",
  "engine": "v2",
  "models_loaded": true
}
```

### Analyze

```
POST /api/v1/mdas/analyze
```

```json
{
  "text": "The customer opened the package."
}
```

Returns voice, sentiment, radar, spam, ABSA, entities, and text statistics. Full response shape is in `src/mdas/api/schemas.py`.

### Errors

| Status | What happened |
|--------|---------------|
| 400 | Bad input (empty text, wrong language, validation failure) |
| 413 | Text too long (over 5,000 characters) |
| 429 | Rate limited (30 requests per minute per IP) |
| 500 | Something broke on our end |
| 504 | Analysis took too long (30 second timeout) |

## What's under the hood

```
src/mdas/
├── api/                  FastAPI app, schemas
├── application/          V1 AnalysisService
├── classification/       V1 spam model (joblib)
├── analysis/             Voice, sentiment, radar, entities
├── core/                 Constants, errors, types
├── nlp/                  spaCy wrapper
├── templates/            HTML (Jinja2 + HTMX)
└── v2/                   V2 engine
    ├── service.py        Drop-in replacement for V1
    ├── spam.py           Trained classifier with SHA-256 verification
    ├── absa.py           Dependency-pattern ABSA
    ├── signals.py        Radar signals
    └── models/           Trained model + metadata
```

## Memory

Everything runs on Render's free tier (512 MB hard limit).

| Component | RSS (MB) | Notes |
|---|---|---|
| spaCy (en_core_web_sm) | ~263 | Voice analysis, NER, dependency parsing |
| sklearn runtime | ~110 | LinearSVC, TF-IDF vectorizer (shared by spam) |
| FastAPI + uvicorn | ~25 | HTTP layer |
| VADER sentiment | ~3 | Lightweight lexicon loader |
| V2 ABSA + signals | ~1 | Pattern matching, lexicon lookup |
| V2 spam model artifact | ~1.6 | Trained model loaded into memory |
| **Total peak** | **~456** | |
| **Remaining headroom** | **~56** | |

Peak measured at 5,000 character input. The 5,000 character limit and single-request recommendation exist because of this.

The training data (SMSSpamCollection, synthetic_diverse.tsv) lives in the git repo under `v2-training-data/` for documentation and reproducibility. It is not deployed to Render and does not consume any runtime memory. Only the trained model artifact (`spam_v2.joblib`) gets loaded.

## Constraints

- 512 MB RAM total (OS + Python + spaCy + models + app)
- 5,000 character input limit
- English only
- No authentication (rate limiting only)
- Single concurrent request recommended

## Environment variables

| Variable | What it does |
|---|---|
| `MDAS_V2` | `true` for V2 engine, `false` for V1. Default: `false` |
| `MDAS_TIMEOUT` | Request timeout in seconds. Default: `30` |
| `PYTHONPATH` | Set to `src` for module resolution |

Rollback to V1: set `MDAS_V2=false` in Render's dashboard. No code change needed.

## Security

- Spam model is SHA-256 verified before loading (pickle files can execute arbitrary code if tampered with)
- 30 second request timeout
- Security headers (HSTS, nosniff, DENY framing)
- No stack traces sent to clients
- No file uploads, no shell commands, no eval

Full audit in `SECURITY.md`.

## Deployment

```yaml
# render.yaml
services:
  - type: web
    name: mdas
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt && python -m spacy download en_core_web_sm
    startCommand: uvicorn mdas.api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONPATH
        value: "src"
      - key: MDAS_V2
        value: "true"
      - key: MDAS_TIMEOUT
        value: "30"
```

## Web UI

| Route | What it is |
|-------|------------|
| `/` | Landing page |
| `/app` | Text analyzer (HTMX) |
| `/api-docs` | API docs |
