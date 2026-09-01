# MDAS � Multi-Dimensional Analysis System

MDAS is a modular-monolith NLP microservice designed to provide deep structural and semantic understanding of English text. It goes beyond simple document classification to understand **what each clause is doing**, extracting grammatical evidence for active, passive, and linking constructions.

## Core MVP Features

MDAS is currently locked for its MVP release with a strict focus on grammatical and semantic visibility.

### 1. P0: Clause-Level Voice Analysis (Primary Capability)
Unlike simple binary document classifiers, MDAS parses sentences into individual clauses and evaluates each predicate:
* **Active**: Tracks subjects, verbs, and objects.
* **Passive**: Identifies both agentive and agentless passives, parsing auxiliaries and main verbs.
* **Linking**: Identifies copular verbs and predicate complements (e.g., "The packaging was excellent").
* **Evidence**: Extracts the exact text spans corresponding to the Subject, Verb, Object, Auxiliary, Agent, Copula, and Complement for every predicted clause.

### 2. P1: Aspect-Based Sentiment Analysis (ABSA)
Identifies explicit aspects (e.g., "packaging", "delivery") and their descriptive modifiers, assigning a sentiment score directly to the aspect based on context.

### 3. P1: Operational Radar Signals
Provides a normalized (0.0 to 1.0) 5-axis signal output for:
* **Sentiment**: Overall document polarity.
* **Toxicity**: Detection of harmful or aggressive language.
* **Sarcasm**: (Experimental/Future Scope)
* **Urgency**: Algorithmic assessment based on keywords, sentiment, and churn presence.
* **Churn Risk**: Signals indicating intent to cancel or leave.

### 4. P2: Spam Detection
A lightweight, pure Scikit-Learn (TF-IDF + LinearSVC) classifier trained specifically for ham/spam detection with a highly conservative false-positive rate.

---

## Future Scope (Archived Features)

To meet the strict memory constraints of the MVP deployment environment, the following experimental and heavy models have been explicitly excluded from the production inference path and archived:
* **Intent Classification**: Temporarily removed.
* **Transformers (MiniLM/PyTorch)**: Stripped from the runtime to save ~300MB+ of resident RAM.
* **Topic/Category Classification**: Archived.

## Input Limits & Render Free Limitations

Because MDAS is deployed on a **512 MB Render Free Tier**, memory footprint (Resident Set Size) is strictly managed.
* The spaCy dependency parser requires significant memory for very large documents.
* **Hard Input Limit**: The API will reject inputs exceeding **5,000 characters**.
* For larger documents, clients must chunk text by paragraph before sending it to MDAS.

## Supported Language

MDAS currently supports **English** only. It will return an HTTP 400 `unsupported_language` error if it detects non-English text.

## API Usage

Start the server:
```bash
python -m src.mdas.api.main
```

Or via Uvicorn:
```bash
uvicorn src.mdas.api.main:app --host 0.0.0.0 --port 8002
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The customer opened the package, and the item was returned."}'
```

**HTMX UI:**
Navigate to `http://127.0.0.1:8002/` to use the built-in visual analyzer.

## Testing & Benchmarks

Run the test suite and Voice benchmark:
```bash
$env:PYTHONPATH="src"
python scratch/run_voice_benchmark.py
```
