"""Accurate sentence-level English active/passive voice analysis."""

PASSIVE_DEPS = {"nsubj:pass", "csubj:pass", "nsubjpass", "csubjpass"}
AGENT_DEPS = {"agent", "obl:agent"}
PASSIVE_AUX_DEPS = {"aux:pass", "auxpass"}
BE_GET_LEMMAS = {"be", "get", "become"}

def _sentence(sent, sid):
    text = sent.text.strip()
    verbs = [t for t in sent if t.pos_ in {"VERB", "AUX"}]
    passive_subjects = [t for t in sent if t.dep_ in PASSIVE_DEPS]
    passive_aux = [t for t in sent if t.dep_ in PASSIVE_AUX_DEPS]
    passive_morph = any("Pass" in t.morph.get("Voice") for t in sent)
    
    # Check for auxiliary BE/GET + Past Participle (VBN) pattern
    has_be_vbn = False
    for i, token in enumerate(sent):
        if token.tag_ == "VBN" and token.pos_ in {"VERB", "ADJ"}:
            for child in token.children:
                if child.lemma_ in BE_GET_LEMMAS and (child.dep_ in PASSIVE_AUX_DEPS or child.dep_ == "aux"):
                    has_be_vbn = True
                    break

    if passive_subjects or passive_aux or passive_morph or has_be_vbn:
        verb = passive_aux[0].head if passive_aux else (passive_subjects[0].head if passive_subjects else (verbs[0] if verbs else None))
        agents = [t for t in sent if t.dep_ in AGENT_DEPS]
        return {
            "sentence_id": sid, "text": text, "voice": "Passive",
            "confidence": 0.96 if (passive_subjects or passive_aux) else 0.88,
            "subject": passive_subjects[0].text if passive_subjects else (sent[0].text if sent else None),
            "verb": verb.text if verb else None,
            "object": None,
            "agent": agents[0].text if agents else None,
            "reason": "Passive subject, auxiliary, or passive participle construction detected."
        }

    subjects = [t for t in sent if t.dep_ in {"nsubj", "csubj"}]
    if subjects and verbs:
        root = next((t for t in sent if t.dep_ == "ROOT" and t.pos_ in {"VERB", "AUX"}), verbs[0])
        objects = [t for t in sent if t.dep_ in {"dobj", "obj", "iobj"} and t.head == root]
        return {
            "sentence_id": sid, "text": text, "voice": "Active",
            "confidence": 0.90 if objects else 0.82,
            "subject": subjects[0].text, "verb": root.text,
            "object": objects[0].text if objects else None, "agent": None,
            "reason": "Active subject and verbal predicate detected."
        }

    # Handle Imperative active commands (e.g. "Fix this immediately", "Please refund my money")
    if verbs:
        root = next((t for t in sent if t.dep_ == "ROOT" and t.pos_ == "VERB"), verbs[0])
        objects = [t for t in sent if t.dep_ in {"dobj", "obj", "iobj"} and t.head == root]
        if root.tag_ in {"VB", "VBP"} or "Imp" in root.morph.get("Mood"):
            return {
                "sentence_id": sid, "text": text, "voice": "Active",
                "confidence": 0.85,
                "subject": "[You (Implied)]", "verb": root.text,
                "object": objects[0].text if objects else None, "agent": None,
                "reason": "Imperative active command detected with implied subject."
            }

    return {
        "sentence_id": sid, "text": text, "voice": "Uncertain", "confidence": None,
        "subject": None, "verb": verbs[0].text if verbs else None, "object": None, "agent": None,
        "reason": "Insufficient structural evidence for a definitive voice decision."
    }

def analyze_voice(doc):
    details = [_sentence(sent, i) for i, sent in enumerate(doc.sents, 1)]
    counts = {"active": 0, "passive": 0, "uncertain": 0}
    for item in details:
        counts[item["voice"].lower()] += 1
    classified = counts["active"] + counts["passive"]
    return {
        "summary": {
            **counts,
            "classified_sentences": classified,
            "passive_ratio": round(counts["passive"]/classified, 3) if classified else 0.0,
        },
        "sentences": details,
    }
