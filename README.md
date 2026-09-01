# MDAS — Multidimensional Text Analysis System

MDAS provides clause-level voice analysis, radar signals, ABSA, sentiment, and spam classification via a REST API. No API key is required for local or open deployment testing.

## Limits

- Maximum payload: 5,000 characters (hard-capped to preserve the 512 MB memory boundary for free-tier deployments).
- Only English text is supported in the MVP.
- No authentication required.

## Health Check

```
GET /api/v1/mdas/health
```

Returns the current status and whether models are loaded.

**Response (200 OK)**
```json
{
  "status": "online",
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
    "method": "tfidf_linear_svc",
    "model_version": "v1"
  },
  "absa": []
}
```

## Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_FAILED | JSON validation failure, empty text, or unsupported language. |
| 400 | BAD_REQUEST | Text field is empty or missing. |
| 413 | PAYLOAD_TOO_LARGE | Text exceeds the 5,000 character limit. |
| 429 | RATE_LIMITED | Too many requests (30/min per IP). |
| 500 | ANALYSIS_FAILED | Analysis service unavailable or internal failure. |

## Features

### Voice Analysis
Clause-level Active / Passive / Linking classification with grammatical evidence extraction.

Evidence fields: Subject, Verb, Auxiliary, Object, Agent, Copula, Complement

Each clause includes the source text and a classification label. The summary_label is active, passive, linking, or mixed.

### Radar Signals
Normalized 0.0–1.0 signal strengths:

- **Sentiment** — Lexicon-based compound polarity, normalized to 0–1
- **Toxicity** — Lexical harmful language detection
- **Sarcasm** — Experimental / heuristic only (not a classifier output)
- **Urgency** — Keyword + sentiment signal
- **Churn Risk** — Cancellation intent signals

### ABSA
Aspect-Based Sentiment Analysis using linguistic dependency patterns. Returns aspect-descriptor pairs with polarity (Positive / Negative / Neutral).

### Spam
TF-IDF + LinearSVC classifier. Returns label: ham or spam.

### Sentiment
Lightweight lexicon-based sentiment analysis. Returns positive, negative, or neutral with a compound score from −1 to +1.

> **Note:** The sarcasm radar signal is experimental and heuristic-based. It is not a trained classifier output. Do not rely on it for production decisions.

## Web UI

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/app` | Text analyzer (HTMX) |
| `/api-docs` | API documentation |

## Deployment

MDAS runs on Render Free Tier (512 MB). See `render.yaml` for build and start commands.

## Testing

```bash
PYTHONPATH=src pytest tests/
```
