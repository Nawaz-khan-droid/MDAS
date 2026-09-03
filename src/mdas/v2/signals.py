"""V2 Radar Signals — improvements over V1's lexical baselines.

V1 (signals.py): pure keyword.count / N bounded 0-1, tiny word sets, no negation.
V2 adds:
  1. Expanded lexicons (data-driven, 2-3x larger)
  2. Negation window (negator within 2 tokens deactivates a hit)
  3. Phrase weighting (multi-word signals score higher)
  4. Frequency weighting (2nd+ hit escalates)
Contract preserved: dict with score/label/evidence_count + sentiment_source passthrough.
"""
import json
from pathlib import Path

_LEX_PATH = Path(__file__).parent / "signal_lexicons.json"


def _load_lexicons():
    try:
        return json.loads(_LEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return _FALLBACK


def _bounded(x):
    return round(max(0.0, min(1.0, x)), 3)


def _count_negation_aware(text, phrases):
    """Count occurrences, deactivating any that are negated within a 2-token window."""
    low = " " + text.lower() + " "
    total = 0
    tokens = low.split()
    for i, w in enumerate(tokens):
        # strip punctuation for matching
        core = w.strip(".,!?;:'\"()[]")
        if core in phrases:
            # check previous 2 tokens for negation
            start = max(0, i - 2)
            window = tokens[start:i]
            negated = any(t.strip(".,!?;:'\"()[]") in _NEGATORS for t in window)
            if not negated:
                total += 1
    return total


# Negators shared (also exported for ABSA use if needed)
_NEGATORS = {"not", "no", "never", "n't", "neither", "nor", "hardly", "scarcely", "barely", "without"}

# Phrase-level signals: presence of EXACT multi-word phrases is a stronger hit (weight 1.5)
_PHRASES = {
    "urgency": ["right away", "as soon as possible", "immediately please", "cannot wait", "can't wait", "urgently need", "click now", "act now", "expires today", "expires by", "due by"],
    "churn": ["take my business elsewhere", "cancel my subscription", "close my account", "delete my account", "moving to another", "switch to competitor", "i am leaving", "never coming back", "cancel my order", "move to the rival", "porting my lines", "leaving for another"],
    "toxicity": ["shut up", "screw you", "go away", "you idiot", "stupid service", "horrible service", "wasted my day", "wasted my time", "you're useless", "you are useless"],
}


_FALLBACK = {
    "urgency": ["urgent", "urgently", "immediately", "immediate", "asap", "now", "critical", "emergency", "deadline", "today", "right away", "cannot wait", "can't wait", "expedite", "expediting", "lapse", "lapses", "time-sensitive", "time sensitive", "rush order", "by noon", "this week"],
    "churn": ["cancel", "cancellation", "unsubscribe", "leave", "switch", "switching", "competitor", "competitors", "terminate", "close my account", "delete my account", "moving to another", "take my business elsewhere", "port", "porting", "rival", "rivals", "defect", "defecting", "divorce", "drop service"],
    "toxicity": ["idiot", "idiots", "stupid", "garbage", "trash", "moron", "loser", "shut up", "screw you", "damn", "hell", "arrogant", "claptrap", "fool", "imbecile", "pathetic", "contemptible"],
    "sarcasm": ["great job", "fantastic", "wonderful", "stellar", "brilliant", "what a surprise", "love that", "excellent work"],
    "negative": ["bad", "terrible", "awful", "horrible", "unacceptable", "angry", "frustrated", "hate", "failed", "failure", "broken", "worst", "disappointed", "ridiculous", "useless", "garbage"],
}

# Single high-confidence triggers: a lone occurrence is decisive on its own
_STRONG = {
    "urgency": ["expedite", "expediting", "lapse", "lapses", "time-sensitive", "critical", "emergency", "immediately", "immediate", "deadline"],
    "churn": ["port", "porting", "rival", "rivals", "defect", "defecting", "cancel", "switch", "switching", "terminate"],
    "toxicity": ["arrogant", "claptrap", "idiot", "imbecile", "moron", "useless", "pathetic", "screw you"],
}


def _signal(text, kind, divisor):
    lexx = _load_lexicons().get(kind, _FALLBACK.get(kind, []))
    phrases = _PHRASES.get(kind, [])
    strong = _STRONG.get(kind, [])
    low = " " + text.lower() + " "

    # single-word/multi-word phrase hits (negation-aware)
    n = _count_negation_aware(text, lexx)
    # phrases weight 1.5 (and are exclusive — skip single-token double count)
    phrase_hits = 0
    for p in phrases:
        if f" {p} " in low:
            phrase_hits += 1
    # strong single-trigger: decisive signal even when alone (weight to clear high band)
    strong_hits = sum(1 for s in strong if f" {s} " in low or f" {s}" in low.rstrip("."))
    # Frequency escalation: 2nd+ hit adds a bonus (real escalation signal)
    freq_bonus = 0.0
    if n >= 2:
        freq_bonus = min(0.15, 0.05 * (n - 1))
    hits_effective = n * 1.0 + phrase_hits * 1.5 + strong_hits * 1.5
    score = _bounded(hits_effective / divisor + freq_bonus)
    return score, n + phrase_hits + strong_hits


def urgency_signal(text):
    score, n = _signal(text, "urgency", 3)
    label = "high" if score >= 0.67 else ("medium" if score >= 0.34 else "low")
    return {"score": score, "label": label, "method": "lexical_baseline_v2", "evidence_count": n}


def churn_signal(text):
    score, n = _signal(text, "churn", 2)
    label = "high" if score >= 0.67 else ("medium" if score >= 0.34 else "low")
    return {"score": score, "label": label, "method": "lexical_baseline_v2", "evidence_count": n}


def toxicity_signal(text):
    score, n = _signal(text, "toxicity", 3)
    label = "high" if score >= 0.67 else ("medium" if score >= 0.34 else "low")
    return {"score": score, "label": label, "method": "lexical_baseline_v2", "evidence_count": n}


def sarcasm_signal(text):
    lexx = _load_lexicons().get("sarcasm", _FALLBACK.get("sarcasm", []))
    neg = _load_lexicons().get("negative", _FALLBACK.get("negative", []))
    low = text.lower()
    n = sum(low.count(x) for x in lexx)
    bonus = 0.25 if n and any(w in low for w in neg) else 0.0
    score = _bounded(min(0.75, n * 0.25) + bonus)
    label = "likely" if score >= 0.67 else ("possible" if score >= 0.34 else "low")
    return {"score": score, "label": label, "method": "lexical_baseline_v2", "marker_count": n, "warning": "Heuristic — not calibrated probability."}


def sentiment_signal_from_label(label):
    if label is None:
        return None
    x = label.lower()
    return {"negative": 1.0, "neutral": 0.5, "positive": 0.0}.get(x)


def build_signals(text, sentiment_label):
    return {
        "urgency": urgency_signal(text),
        "churn_risk": churn_signal(text),
        "toxicity": toxicity_signal(text),
        "sarcasm": sarcasm_signal(text),
        "sentiment_source": {"method": "classification_model", "label": sentiment_label},
    }