import re
from mdas.core.types import Entity

PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "PHONE": re.compile(r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s])\d{3}[-.\s]\d{4}(?!\d)"),
    "ORDER_ID": re.compile(r"\b(?:order|ord)\s*(?:id|#)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9_-]{2,})\b", re.I),
    "TRANSACTION_ID": re.compile(r"\b(?:transaction|trans|txn)\s*(?:id|#)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9_-]{2,})\b", re.I),
}

def extract_entities(doc):
    results = [Entity(ent.text, ent.label_, ent.start_char, ent.end_char, "spacy") for ent in doc.ents]
    existing = {(e.start, e.end, e.label) for e in results}
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(doc.text):
            key = (match.start(), match.end(), label)
            if key not in existing:
                value = match.group(1) if label in {"ORDER_ID", "TRANSACTION_ID"} else match.group(0)
                results.append(Entity(value, label, match.start(), match.end(), "regex"))
    return sorted(results, key=lambda x: (x.start, x.end))
