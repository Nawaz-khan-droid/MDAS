# MDAS — Multidimensional Text Analysis System

MDAS is a lightweight NLP API that provides clause-level voice analysis, aspect-based sentiment (ABSA), radar signals (toxicity/urgency/churn/sarcasm), spam classification, and lexicon-based sentiment — all running on a 512 MB free-tier deployment with no API keys required.

**Live:** `https://mdas-0x3n.onrender.com`
**API base:** `POST /api/v1/mdas/analyze`

---

## Quick Start

```bash
# Local development
pip install -r requirements.txt
python -m spacy download en_core_web_sm
PYTHONPATH=src uvicorn mdas.api.main:app --reload

# Run tests
PYTHONPATH=src pytest tests/
```

**cURL**
```bash
curl -X POST https://mdas-0x3n.onrender.com/api/v1/mdas/analyze \
     -H "Content-Type: application/json" \
     -d '{"text": "The customer opened the package."}'
```

---

## Engine Versions

MDAS ships two engines behind a single API. The `MDAS_V2` environment variable controls which runs.

| Component | V1 | V2 |
|---|---|---|
| **Spam** | 123 samples, 83.5% acc, hard spam/ham | 7,699 samples, 98.9% acc, margin-triage (spam/ham/needs_human_triage) |
| **ABSA** | Adjective-on-noun patterns (7/11) | Verb-predicate + 8 extraction patterns (10/11 on matched set; **1/12 on independent unseen**) |
| **Radar** | Raw keyword count | Negation-aware, phrase weighting, strong-trigger escalation |
| **Voice** | Dependency rules | Shared V1 — unchanged |
| **Sentiment** | VADER lexicon | Shared V1 — unchanged |
| **Entities** | spaCy NER | Shared V1 — unchanged |

V2 is an extension of V1, not a separate application. It reuses the same API contract, spaCy backend, voice rules, entity extraction, and VADER sentiment. One engine runs per deployment.

### What V2 changes

- **`src/mdas/v2/spam.py`** — TF-IDF + LinearSVC with margin-based triage. Trained on UCI SMS Spam Collection (5,574) + domain augmentation (125) + synthetic diversity (2,000) = 7,699 samples. SHA-256 hash verified before loading.
- **`src/mdas/v2/absa.py`** — 8 dependency extraction patterns (P1-P8): amod, acomp, VBN passive, compound nouns, relative clauses, verb-predicate sentiment, xcomp+advmod, oprd resultatives. Uses `descriptor_lexicon.json` (600+ words) and `verb_lexicon.json` (positive/negative event verbs).
- **`src/mdas/v2/signals.py`** — Lexicon-based radar with negation window, phrase-level weighting (1.5x), strong-trigger escalation, and frequency bonus.

---

## Honest Assessment

### What works well

- **Spam** — The strongest component. 98.9% accuracy on holdout (1,155 test), 98.3% on a 126-text domain benchmark. Margin triage catches ambiguous cases instead of mislabeling. FP rate: 1/126 (V1 was 6/126). This is a trained model with proper train/test split and reproducible metrics.
- **Voice** — Dependency-structure rules. 7/8 on unseen text. Genuinely robust because it relies on syntactic patterns, not per-word lexicons.
- **Sentiment** — VADER-based, 7/9 on benchmark. Consistent between V1 and V2.

### What does NOT generalize

- **ABSA** — 10/11 on the matched benchmark set, but **1/12 on independent held-out text**. The patterns and lexicon were tuned to known phrasings. Novel verbs (shred, creak, bow, chafe, resist, trap, release, breathe, corrode, bounce) are largely missed. ABSA is a coverage system, not a generalizable one.
- **Radar (toxicity/urgency/churn)** — Improved coverage on matched test sentences, but improvements are fit-to-sample. Lexicon additions were chosen to hit specific test cases. Real-world out-of-distribution robustness is not demonstrated. Toxicity has a known regression: "idiot... Screw you" scores 0.33 (low) in V2 vs 1.0 (high) in V1.
- **Sarcasm** — Heuristic only in both V1 and V2. Not a trained classifier. 0/1 in both versions.

### Bottom line

If the product needs robust ABSA or radar across arbitrary unseen prose, rule-based and lexicon-based systems are insufficient. That requires a trained statistical component or an LLM. The measurable, defensible V2 wins are **spam** (trained + held-out eval) and **voice** (dependency rules). ABSA/radar improvements are coverage-only.

---

## API Reference

### Health Check

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

**Request**
```json
{ "text": "The customer opened the package." }
```

**Response**
```json
{
  "analysis_id": "uuid",
  "status": "success",
  "language": { "code": "en", "label": "English" },
  "statistics": {
    "words": 6, "characters": 30, "sentences": 1,
    "tokens": 7, "paragraphs": 1, "reading_time": "< 1 min"
  },
  "linguistics": {
    "voice": {
      "summary_label": "active",
      "method": "dependency_rules",
      "sentences": [{
        "text": "The customer opened the package",
        "label": "active",
        "evidence": {
          "subject": "customer", "verb": "opened",
          "object": "package", "text": "customer opened package"
        }
      }]
    },
    "entities": []
  },
  "sentiment": { "label": "neutral", "score": 0.0, "method": "lexicon_rules" },
  "radar": {
    "sentiment": 0.5, "toxicity": 0.0, "sarcasm": 0.0,
    "urgency": 0.1, "churn_risk": 0.1
  },
  "spam": {
    "label": "ham", "confidence": 0.0,
    "method": "tfidf_linear_svc_v2", "model_version": "2.0"
  },
  "absa": []
}
```

### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_FAILED | JSON validation failure, empty text, or unsupported language |
| 400 | BAD_REQUEST | Text field is empty or missing |
| 400 | UNSUPPORTED_LANGUAGE | Text is not English |
| 413 | PAYLOAD_TOO_LARGE | Text exceeds 5,000 characters |
| 429 | RATE_LIMITED | Too many requests (30/min per IP) |
| 500 | ANALYSIS_FAILED | Analysis service unavailable or internal failure |
| 504 | TIMEOUT | Analysis exceeded configured timeout |

---

## Feature Details

### Voice Analysis
Clause-level Active / Passive / Linking classification using spaCy dependency parsing. Evidence fields: Subject, Verb, Auxiliary, Object, Agent, Copula, Complement. Summary label: active, passive, linking, or mixed.

**Accuracy:** 84.6% overall (atomic clauses ~100%, multi-clause ~72%). 7/8 on independent unseen text.

### Spam Classification
TF-IDF + LinearSVC with margin-based triage. When |margin| <= 0.2, the model returns `needs_human_triage` instead of a hard label — reducing false positives on ambiguous text.

**Training data:** 7,699 samples (UCI SMS Spam Collection + domain augmentation + synthetic). See `v2-training-data/` for the full dataset.

| Metric | Holdout (1,155) | Domain Benchmark (126) |
|--------|-----------------|----------------------|
| Accuracy | 98.87% | 98.31% |
| Spam F1 | 97.52% | 96.15% |
| False Positives | 1 | 1 |
| False Negatives | — | 1 |
| Triaged | 13 | 8 |

### ABSA (Aspect-Based Sentiment Analysis)
Dependency-pattern extraction returning aspect-descriptor pairs with polarity (Positive / Negative / Neutral).

**Honest caveat:** 10/11 on matched test set, 1/12 on independent unseen text. Coverage-only, not generalizable.

### Radar Signals
Normalized 0.0–1.0 signal strengths:

| Signal | Method | Honest Assessment |
|--------|--------|-------------------|
| Sentiment | VADER compound polarity | Consistent, 7/9 |
| Toxicity | Lexical harmful language detection | Improved coverage, has regressions on some phrases |
| Sarcasm | Experimental heuristic | Weak in both V1 and V2, not reliable |
| Urgency | Keyword + phrase-level weighting | Improved coverage, fit-to-sample |
| Churn Risk | Cancellation intent signals | Improved coverage, fit-to-sample |

### Sentiment
Lightweight lexicon-based (VADER). Returns positive, negative, or neutral with a compound score from −1 to +1.

---

## Constraints

### Hard Limits
- **512 MB RAM** — Render Free Tier ceiling. V2 peak: 456 MB (56 MB headroom).
- **5,000 characters** — Hard-capped input limit.
- **English only** — Non-English text is rejected with HTTP 400.
- **No PyTorch** — Excluded to stay within memory budget.
- **No authentication** — MVP API is open. Rate limiting (30 req/min/IP) mitigates abuse.

### Known Limitations
- **ABSA/radar do not generalize** — Pattern/lexicon systems increase coverage of known forms but fail on novel phrasing.
- **Sarcasm detection is unreliable** — Heuristic only, not a trained classifier.
- **Memory headroom is tight** — 56 MB at peak. Concurrent requests risk OOM on free tier.
- **LinearSVC is non-deterministic** — Exact holdout numbers vary ~±0.2% between retrains (liblinear backend).
- **Single concurrent request recommended** — Free tier memory constraints.

### What Was Intentionally Removed
| Component | Reason |
|-----------|--------|
| Intent Classification | Requires PyTorch (~300 MB+) |
| MiniLM / SentenceTransformers | Training-only dependency, not needed in production |
| NLTK VADER | Replaced with lightweight lexicon loader (saves 107 MB) |

---

## Project Structure

```
src/mdas/
├── api/
│   ├── main.py              # FastAPI app (V1/V2 feature flag, timeout, logging)
│   └── schemas.py           # Pydantic models (AnalysisResponse)
├── application/
│   └── analysis_service.py  # V1 AnalysisService
├── classification/
│   ├── model.py             # V1 TextClassifier (joblib)
│   └── registry.py          # ModelRegistry
├── analysis/
│   ├── language.py          # langdetect wrapper
│   ├── linguistics.py       # Voice + NER
│   ├── lightweight_sentiment.py  # VADER
│   ├── signals.py           # V1 radar signals
│   └── statistics.py        # Word/sent counts
├── core/
│   ├── constants.py         # MAX_TEXT_LENGTH, etc.
│   ├── errors.py            # Exception classes
│   └── types.py             # Internal dataclasses
├── nlp/
│   └── spacy_backend.py     # spaCy pipeline wrapper
├── templates/               # Jinja2 HTML templates
└── v2/                      # V2 engine (drop-in replacement)
    ├── service.py           # V2AnalysisService
    ├── absa.py              # V2 ABSA patterns
    ├── signals.py           # V2 radar signals
    ├── spam.py              # V2 spam classifier (SHA-256 verified)
    ├── descriptor_lexicon.json
    ├── verb_lexicon.json
    ├── signal_lexicons.json
    └── models/
        ├── spam_v2.joblib   # Trained model
        └── spam_v2.json     # Metadata + SHA-256 prefix

v2-training-data/            # Training datasets (reproducibility)
├── SMSSpamCollection        # UCI SMS Spam Collection (5,574 msgs)
├── synthetic_diverse.tsv    # Synthetic diversity samples (2,000)
└── domain_augmentation.py   # Domain-specific examples (125)
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MDAS_V2` | `false` | Set to `true` to use the V2 engine |
| `MDAS_TIMEOUT` | `30` | Request timeout in seconds |
| `PYTHONPATH` | — | Set to `src` for module resolution |

**Rollback:** Set `MDAS_V2=false` in Render environment variables to instantly switch to V1. No code change needed.

---

## Security

- **Model integrity** — V2 spam model is SHA-256 hash verified before loading (defense against pickle deserialization attacks).
- **Request timeout** — 30s timeout prevents request hanging (configurable via `MDAS_TIMEOUT`).
- **Rate limiting** — 30 requests/min per IP with `Retry-After` header.
- **Security headers** — HSTS, X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Referrer-Policy.
- **No stack traces to clients** — Errors logged server-side, generic messages returned.
- **Input validation** — Pydantic schema, max 5,000 chars, empty text rejected.
- **No file upload, no shell commands, no eval** — Text-only API.

See `SECURITY.md` for the full security audit.

---

## Deployment

MDAS runs on Render Free Tier (512 MB). See `render.yaml` for build and start commands.

```yaml
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

---

## Testing

```bash
# V1 tests
PYTHONPATH=src pytest tests/unit/

# V2 tests (31 tests: spam, ABSA, signals, integration)
PYTHONPATH=src pytest tests/v2/

# All tests
PYTHONPATH=src pytest tests/
```

---

## Web UI

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/app` | Text analyzer (HTMX) |
| `/api-docs` | API documentation |

---

## License

See repository for license details.
