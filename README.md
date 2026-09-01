# MDAS — Multi-Dimensional Analysis System

MDAS is a modular-monolith NLP microservice that provides deep structural and semantic understanding of English text. It goes beyond simple document classification to understand **what each clause is doing**, extracting grammatical evidence for active, passive, and linking constructions.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn mdas.api.main:app --host 0.0.0.0 --port 8002
```

Open `http://localhost:8002/` for the visual analyzer, or `http://localhost:8002/api-docs` for API documentation.

## Features

### P0: Clause-Level Voice Analysis
The core capability. MDAS parses sentences into individual clauses and classifies each predicate:
- **Active** — tracks subjects, verbs, and objects
- **Passive** — identifies agentive and agentless passives, parsing auxiliaries and main verbs
- **Linking** — identifies copular verbs and predicate complements

Every clause includes extracted grammatical evidence: Subject, Verb, Object, Auxiliary, Agent, Copula, Complement.

### P1: Operational Radar Signals
A normalized (0.0–1.0) 5-axis signal output for downstream routing:
| Signal | Method |
|--------|--------|
| Sentiment | Lexicon-based compound polarity |
| Toxicity | Lexical harmful language detection |
| Sarcasm | Experimental / heuristic only |
| Urgency | Keyword + sentiment signal |
| Churn Risk | Cancellation intent signals |

### P1: Aspect-Based Sentiment Analysis (ABSA)
Extracts explicit aspects (e.g., "packaging", "delivery") and their descriptive modifiers, assigning sentiment polarity per aspect.

### P2: Spam Detection
TF-IDF + LinearSVC classifier trained for ham/spam detection with a conservative false-positive rate.

### Language & Statistics
Word count, sentence count, token count, reading time, and language detection.

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/mdas/health` | GET | Health check |
| `/api/v1/mdas/analyze` | POST | Full analysis |

**Request:**
```json
{ "text": "The customer opened the package." }
```

**Response includes:** language, statistics, voice (per clause), sentiment, radar signals, ABSA, spam classification.

See `/api-docs` in the browser for the full schema and error codes.

## Deployment

MDAS is designed for **Render Free Tier (512 MB)**. Key constraints:
- **Hard input limit:** 5,000 characters (rejects with HTTP 413)
- **Language:** English only (non-English returns HTTP 400)
- **Memory:** Peak usage ~474 MB at 5K input with 38 MB headroom

For larger documents, chunk text by paragraph before sending.

## Testing

```bash
PYTHONPATH=src pytest tests/
```

## Project Structure

```
src/mdas/
├── api/            # FastAPI routes and schemas
├── application/    # Analysis service (orchestrator)
├── analysis/       # Voice, sentiment, signals, statistics, ABSA
├── classification/ # Spam classifier, registry
├── core/           # Constants, errors, config
├── nlp/            # spaCy backend
└── templates/      # Jinja2 + HTMX UI
```

## License

See repository for license details.
