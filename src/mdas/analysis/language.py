from collections import Counter

ENGLISH_MARKERS = {
    "the", "and", "is", "are", "to", "of", "in", "for", "with", "this", "that",
}

def identify_english(text: str) -> dict:
    words=[w.lower() for w in text.split() if w.isalpha()]
    hits=sum(w in ENGLISH_MARKERS for w in words)
    score=round(hits/max(1,min(len(words),10)),3)
    return {"language":"en" if score >= 0.1 else "unknown", "label":"English" if score >= 0.1 else "Unknown", "score":score, "method":"lightweight_english_gate", "note":"V1 English-only gate; not a general multilingual language-identification model."}
