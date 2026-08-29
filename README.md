# MDAS — Multi-Dimensional Analysis System

A modular-monolith Python codebase for English text analysis. It separates:

1. Text statistics
2. Linguistic analysis
3. Classification
4. Five-axis MDAS radar signals
5. Structured JSON inference
6. Optional HTTP API

It is intentionally **not an LLM application**.

## What was retained and fixed from the supplied Colab code

The existing MTAS notebook already had separate models for spam, sentiment, intent and content category, a reusable training function, spaCy entity extraction, and a unified inference function. It also contained repeated dataset-loading/training blocks and repeated function definitions; those are consolidated here. The original cleaning step also removed URLs and all non-letter characters before inference, which is inappropriate when later analysis needs IDs, email addresses, money, punctuation or urgency cues. MDAS keeps the raw text for linguistic analysis and uses model pipelines independently.

The voice notebook used a tiny hand-written Active/Passive dataset and TF-IDF over POS-tag strings with Naive Bayes. MDAS does **not** use that as the production voice detector. Voice is analyzed sentence-by-sentence from dependency/morphological structure and can return `Uncertain` instead of forcing a binary answer.

## Scope

V1 targets **English**. The supplied classification datasets are customer/support/social-domain datasets, so the resulting classifiers must be described as domain-specific rather than universal English classifiers. Moderation and document-type classification are deliberately data-driven extensions: they require your own labeled CSVs because the correct taxonomy is project-specific.

Radar axes:

- sentiment
- urgency
- churn risk
- toxicity
- sarcasm

Radar values are normalized signal strengths from `0.0` to `1.0`; they are **not automatically probabilities**.

## NLP Suite relationship

NLP Suite is a separate open-source desktop application. Its documentation covers tokenization, lemmatization, POS, NER, dependency parsing, SVO and sentiment among other tools, and describes Stanza as its recommended pure-Python NLP package.

MDAS therefore provides a backend seam:

- spaCy backend: default because it matches the supplied Colab work.
- Stanza backend: optional, useful for alignment with the NLP stack used/recommended by NLP Suite.
- MDAS does not import NLP Suite GUI/private internals. That would make the application dependent on an unstable application-internal API.

The `integrations/nlp_suite.py` module is the explicit boundary if you later decide to reuse a particular NLP Suite implementation.

## Install

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
python -m spacy download en_core_web_sm
```

Optional Stanza:

```bash
pip install -e ".[stanza]"
python -c "import stanza; stanza.download('en')"
```

## Training data

The project does not silently bundle third-party datasets. Put the datasets described in `data/raw/README.md` into that directory, then run:

```bash
python -m mdas.training.train --data-dir data/raw --output-dir models
```

The trainer uses TF-IDF + LogisticRegression, preserves an untouched test split, reports macro-F1, and stores model metadata beside each artifact.

## Python API

```python
from mdas import MDASAnalyzer

analyzer = MDASAnalyzer.from_directory("models")
result = analyzer.analyze(
    "Oh great, another outage. Fix this immediately or cancel our subscription."
)
print(result.to_dict())
```

## HTTP API

```bash
uvicorn mdas.api.app:app --reload
```

No API key is implemented in this project. This is suitable for a local/project deployment; add authentication/rate limiting before exposing it publicly.

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"My order is late. Please fix this immediately."}'
```

## Large text

Default maximum input is 250,000 characters. Linguistic analysis is sentence-level, so a document can contain both active and passive sentences. The API returns a document summary plus detailed sentence/token/entity records. A frontend should paginate/expand details rather than rendering every record at once.

For documents larger than the configured limit, chunk them at the application boundary on paragraph/sentence boundaries and aggregate the returned summaries.
