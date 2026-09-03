# MDAS — Multidimensional Text Analysis System

MDAS provides clause-level voice analysis, radar signals, ABSA, sentiment, and spam classification via a REST API. No API key is required for local or open deployment testing.

## Engine Versions

MDAS has two engines that share the same API contract. The active engine is controlled by the `MDAS_V2` environment variable.

| | V1 (MVP) | V2 (Current) |
|---|---|---|
| **Spam** | 123 samples, 83.5% acc, hard spam/ham only | 7,699 samples, 98.9% acc, margin-triage (spam/ham/needs_human_triage) |
| **ABSA** | Adjective-on-noun patterns only | Verb-predicate, reduced clauses, resultatives, negation-aware |
| **Radar** | Raw keyword count, no negation handling | Negation-aware, phrase weighting, strong-trigger escalation |
| **Voice** | Dependency rules (active/passive/linking/mixed) | Same (shared V1 code, unchanged) |
| **Sentiment** | VADER lexicon scoring | Same (shared V1 code, unchanged) |
| **Entities** | spaCy NER (ORG/LOCATION/DATE/PRODUCT/PERSON) | Same (shared V1 code, unchanged) |

V2 reuses V1's API schema (`AnalysisResponse`), spaCy backend, voice rules, entity extraction, and VADER sentiment. It replaces the spam model, ABSA patterns, and radar signals with improved versions.

### What V2 changes specifically

- **`src/mdas/v2/spam.py`** — TF-IDF + LinearSVC with margin-based triage. Trained on UCI SMS Spam Collection (5,574) + domain augmentation (125) + synthetic diversity (2,000) = 7,699 samples. SHA-256 hash verified before loading.
- **`src/mdas/v2/absa.py`** — Dependency-pattern ABSA with 8 extraction patterns (P1-P8): amod, acomp, VBN passive, compound nouns, relative clauses, verb-predicate sentiment, xcomp+advmod, oprd resultatives. Uses `descriptor_lexicon.json` (600+ words) and `verb_lexicon.json` (positive/negative event verbs).
- **`src/mdas/v2/signals.py`** — Lexicon-based radar with negation window, phrase-level weighting (1.5x), strong-trigger escalation, and frequency bonus. Signals: urgency, churn, toxicity, sarcasm.

### Honest limitations

ABSA and radar are hand-curated pattern/lexicon systems. They increase coverage of known forms but do NOT generalize to arbitrary unseen phrasing. The spam model is the only component with a proper trained-and-evaluated holdout test. Voice rules are dependency-structure based and transfer well.

## Limits

- Maximum payload: 5,000 characters (hard-capped to preserve the 512 MB memory boundary for free-tier deployments).
- Only English text is supported in the MVP.
- No authentication required.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MDAS_V2` | `false` | Set to `true` to use the V2 engine |
| `MDAS_TIMEOUT` | `30` | Request timeout in seconds |
| `PYTHONPATH` | — | Set to `src` for module resolution |

## Health Check

```
GET /api/v1/mdas/health
```

Returns the current status, which engine is active, and whether models are loaded.

**Response (200 OK)**
```json
{
  "status": "online",
  "engine": "v2",
  "models_loaded": true
}
```

## Analyze Text

```
POST /api/v1/mdas/analyze
```

**Request Body (JSON)**
```json
{
  "text": "The customer opened the package, and the item was returned."
}
```

**Example cURL**
```bash
curl -X POST https://mdas-0x3n.onrender.com/api/v1/mdas/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "The customer opened the package."}'
```

**Response (200 OK)**
```json
{
  "analysis_id": "uuid",
  "status": "success",
  "language": {
    "code": "en",
    "label": "English"
  },
  "statistics": {
    "words": 6,
    "characters": 30,
    "sentences": 1,
    "tokens": 7,
    "paragraphs": 1,
    "reading_time": "< 1 min"
  },
  "linguistics": {
    "voice": {
      "summary_label": "active",
      "method": "dependency_rules",
      "sentences": [
        {
          "text": "The customer opened the package",
          "label": "active",
          "evidence": {
            "subject": "customer",
            "verb": "opened",
            "object": "package",
            "text": "customer opened package"
          }
        }
      ]
    },
    "entities": []
  },
  "sentiment": {
    "label": "neutral",
    "score": 0.0,
    "method": "lexicon_rules"
  },
  "radar": {
    "sentiment": 0.5,
    "toxicity": 0.0,
    "sarcasm": 0.0,
    "urgency": 0.1,
    "churn_risk": 0.1
  },
  "spam": {
    "label": "ham",
    "confidence": 0.0,
    "method": "tfidf_linear_svc_v2",
    "model_version": "2.0"
  },
  "absa": []
}
```

## Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_FAILED | JSON validation failure, empty text, or unsupported language. |
| 400 | BAD_REQUEST | Text field is empty or missing. |
| 400 | UNSUPPORTED_LANGUAGE | Text is not English. |
| 413 | PAYLOAD_TOO_LARGE | Text exceeds the 5,000 character limit. |
| 429 | RATE_LIMITED | Too many requests (30/min per IP). |
| 500 | ANALYSIS_FAILED | Analysis service unavailable or internal failure. |
| 504 | TIMEOUT | Analysis exceeded the configured timeout. |

## Features

### Voice Analysis
Clause-level Active / Passive / Linking classification with grammatical evidence extraction.

Evidence fields: Subject, Verb, Auxiliary, Object, Agent, Copula, Complement

Each clause includes the source text and a classification label. The summary_label is active, passive, linking, or mixed.

### Radar Signals
Normalized 0.0–1.0 signal strengths:

- **Sentiment** — Lexicon-based compound polarity, normalized to 0–1
- **Toxicity** — Lexical harmful language detection (V2: negation-aware, strong-trigger escalation)
- **Sarcasm** — Experimental / heuristic only (not a classifier output)
- **Urgency** — Keyword + phrase-level weighting (V2: expanded hallmarks, strong-trigger tier)
- **Churn Risk** — Cancellation intent signals (V2: expanded lexicon, strong-trigger tier)

### ABSA
Aspect-Based Sentiment Analysis using linguistic dependency patterns. Returns aspect-descriptor pairs with polarity (Positive / Negative / Neutral).

V1: adjective-on-noun patterns only.
V2: adds verb-predicate, reduced clauses, resultatives, negation-aware polarity, expanded descriptor lexicon (600+ words).

### Spam
TF-IDF + LinearSVC classifier with margin-based triage.

- **V1**: 123 training samples, 83.5% accuracy, hard spam/ham labels only.
- **V2**: 7,699 training samples (UCI SMS + domain augmentation + synthetic), 98.9% accuracy, margin-based triage (spam/ham/needs_human_triage). SHA-256 hash verified before loading.

### Sentiment
Lightweight lexicon-based sentiment analysis. Returns positive, negative, or neutral with a compound score from −1 to +1.

> **Note:** The sarcasm radar signal is experimental and heuristic-based. It is not a trained classifier output. Do not rely on it for production decisions.

## Web UI

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/app` | Text analyzer (HTMX) |
| `/api-docs` | API documentation |

## Project Structure

```
src/mdas/
├── api/
│   ├── main.py          # FastAPI app (V1/V2 feature flag)
│   └── schemas.py       # Pydantic models (AnalysisResponse)
├── application/
│   └── analysis_service.py  # V1 AnalysisService
├── classification/
│   ├── model.py         # V1 TextClassifier (joblib)
│   └── registry.py      # ModelRegistry
├── analysis/
│   ├── language.py      # langdetect wrapper
│   ├── linguistics.py   # Voice + NER
│   ├── lightweight_sentiment.py  # VADER
│   ├── signals.py       # V1 radar signals
│   └── statistics.py    # Word/sent counts
├── core/
│   ├── constants.py     # MAX_TEXT_LENGTH, etc.
│   ├── errors.py        # Exception classes
│   └── types.py         # Internal dataclasses
├── nlp/
│   └── spacy_backend.py # spaCy pipeline wrapper
├── templates/           # Jinja2 HTML templates
└── v2/                  # V2 engine (drop-in replacement)
    ├── __init__.py
    ├── service.py       # V2AnalysisService
    ├── absa.py          # V2 ABSA patterns
    ├── signals.py       # V2 radar signals
    ├── spam.py          # V2 spam classifier (SHA-256 verified)
    ├── descriptor_lexicon.json  # ABSA polarity lexicon
    ├── verb_lexicon.json        # Verb polarity lexicon
    ├── signal_lexicons.json     # Radar signal words
    └── models/
        ├── spam_v2.joblib   # Trained V2 spam model
        └── spam_v2.json     # Model metadata + SHA-256 prefix
```

## Deployment

MDAS runs on Render Free Tier (512 MB). See `render.yaml` for build and start commands.

**Rollback:** Set `MDAS_V2=false` in Render environment variables to instantly switch back to V1 without code changes.

## Testing

```bash
PYTHONPATH=src pytest tests/
```

## Security

- **Model integrity**: V2 spam model is SHA-256 hash verified before loading (prevents pickle deserialization attacks).
- **Request timeout**: 30s timeout on analysis (configurable via `MDAS_TIMEOUT`).
- **Rate limiting**: 30 requests/min per IP.
- **Security headers**: HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
