# MDAS

A text analysis API that runs on Render's free tier. No API keys, no paid services.

It does clause-level voice analysis, aspect-based sentiment, spam detection, and a handful of radar signals (toxicity, urgency, churn, sarcasm). English only. 5,000 character limit. 512 MB of RAM to work with.

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

There's a V1 and a V2 engine. You pick which one runs with the `MDAS_V2` environment variable. Same API contract, same endpoints — V2 just swaps in better spam detection, ABSA patterns, and radar signals. Voice and sentiment stay the same across both.

| | V1 | V2 |
|---|---|---|
| **Spam** | 123 training samples, 83.5% accuracy | 7,699 samples, 98.9% accuracy, triage for uncertain cases |
| **ABSA** | Adjective-on-noun patterns | Verb-predicate + compound nouns + negation-aware |
| **Radar** | Raw keyword counting | Negation-aware, phrase weighting, strong triggers |
| **Voice** | Dependency rules | Same |
| **Sentiment** | VADER | Same |

V2 builds on top of V1. It's not a rewrite — it's an improvement. You run one or the other, not both.

## What actually works and what doesn't

I'll be straightforward about this.

**Spam detection** is solid. 98.9% on held-out test data, 98.3% on a domain-specific benchmark. It uses margin-based triage — when the model isn't sure, it says "needs human review" instead of guessing wrong. That's the whole point of V2's spam: fewer false positives, and the uncertain cases get flagged instead of misclassified.

**Voice analysis** works well. It's rule-based on dependency parsing, so it transfers to unseen text. 7/8 on independent test sentences. The rules are structural, not word-based, which is why they generalize.

**ABSA and radar** are where I have to be honest. They score well on the test sets I built them against — 10/11 for ABSA, improved coverage on radar signals. But when I tested them on truly independent text (phrasings they hadn't seen during development), ABSA got 1 out of 12 right. The radar improvements are real but they're fit-to-sample: I added words to the lexicon to catch specific test cases. That's coverage, not generalization. If you need ABSA or radar that works on arbitrary new phrasing, you'd need a trained model or an LLM, not hand-tuned patterns.

**Sarcasm** is heuristic-only. It's been 0/1 in both versions. Don't rely on it.

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

Returns voice, sentiment, radar, spam, ABSA, entities, and text statistics. Full response shape is in the code — `src/mdas/api/schemas.py`.

### Errors

| Status | What happened |
|--------|---------------|
| 400 | Bad input — empty text, wrong language, validation failure |
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

Training data lives in `v2-training-data/` — just for reference and reproducibility. The app doesn't load those files at runtime.

## Constraints

The app runs on Render's free tier. That means 512 MB of RAM total — OS, Python, spaCy, the model, everything. Peak usage is around 456 MB, which leaves about 56 MB of headroom. It works, but it's tight. Concurrent requests could push it over.

The 5,000 character limit is there for the same reason. Longer text means more spaCy parsing, more memory, more time. 5K is the safe ceiling.

No authentication. Rate limiting (30/min per IP) is the only protection. English only — other languages get rejected immediately.

## Environment variables

| Variable | What it does |
|---|---|
| `MDAS_V2` | `true` for V2 engine, `false` for V1. Default: `false` |
| `MDAS_TIMEOUT` | Request timeout in seconds. Default: `30` |
| `PYTHONPATH` | Set to `src` for module resolution |

To roll back to V1 on Render: set `MDAS_V2=false` in the dashboard. No code change needed.

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
