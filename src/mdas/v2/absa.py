"""V2 Aspect-Based Sentiment Analysis.

Additive improvements over V1:
  P1,P2,P3  : same as V1 (amod, acomp, VBN+auxpass) — parity preserved
  P4        : compound nouns ("delivery driver was rude" -> aspect=delivery driver)
  P5        : relative clauses ("box that arrived damaged" -> aspect=box, descriptor=damaged)
  P6        : negation window ("not good", "didn't work") -> flipped polarity
  LEX       : expanded descriptor polarity lexicon (~150 words), data-driven
"""
import json
from pathlib import Path

_LEXICON_PATH = Path(__file__).parent / "descriptor_lexicon.json"
_VERB_LEXICON_PATH = Path(__file__).parent / "verb_lexicon.json"


def _load_verbs():
    try:
        data = json.loads(_VERB_LEXICON_PATH.read_text(encoding="utf-8"))
        neg = set(data.get("negative_verbs", []))
        pos = set(data.get("positive_verbs", []))
        return neg, pos, neg | pos
    except Exception:
        return set(), set(), set()


NEG_VERBS, POS_VERBS, ALL_VERBS = _load_verbs()


def _verb_polarity(lemma):
    """Polarity of a verbal predicate by lemma. Returns 'Positive'/'Negative'/None."""
    w = lemma.lower()
    if w in NEG_VERBS:
        return "Negative"
    if w in POS_VERBS:
        return "Positive"
    return None


def _load_lexicon():
    """Load polarity lexicon. Fall back to compact built-in set if file missing."""
    try:
        data = json.loads(_LEXICON_PATH.read_text(encoding="utf-8"))
        return set(data.get("negative", [])), set(data.get("positive", []))
    except Exception:
        neg = {"torn", "broken", "broke", "error", "fail", "terrible", "crashed", "worn",
               "damaged", "scratched", "dented", "soiled", "stained", "bad", "awful", "worst",
               "useless", "disappointed", "frustrated", "faulty", "defective", "slow", "late",
               "missing", "lost", "delayed", "ripped", "unusable", "poor", "cheap", "flimsy"}
        pos = {"excellent", "great", "awesome", "perfect", "good", "new", "clean", "fast",
               "smooth", "nice", "beautiful", "amazing", "outstanding", "well", "quick",
               "durable", "comfortable", "fresh", "genuine", "correct", "proper"}
        return neg, pos


NEG, POS = _load_lexicon()

NEGATORS = {
    "not", "no", "never", "n't", "neither", "nor", "hardly", "scarcely",
    "barely", "without", "non", "un", "dis", "lack", "failed", "failure",
}


def _vader_polarity(word):
    """Lightweight VADER for a single descriptor; used as V1 baseline then overridden by lexicon."""
    # Reuse the V1 lightweight sentiment module for consistency
    from mdas.analysis.lightweight_sentiment import polarity_scores as _vps
    return _vps(word)["compound"]


def _classify(word, negated=False):
    """Polarity for a descriptor, with domain-lexicon override. Returns 'Positive'/'Negative'/'Neutral'."""
    w = word.lower()
    if negated:
        # Simple inversion: if the base word is strongly polar, flip; else keep neutral-ish
        if w in NEG:
            return "Positive"
        if w in POS:
            return "Negative"
    if w in NEG:
        return "Negative"
    if w in POS:
        return "Positive"
    # VADER-lite fallback
    score = _vader_polarity(w)
    if score >= 0.05:
        return "Positive"
    if score <= -0.05:
        return "Negative"
    return "Neutral"


def _has_negation_window(token, window=2):
    """True if a negation token occurs within `window` tokens to the left."""
    if not token.doc:
        return False
    start = max(token.i - window, 0)
    for t in token.doc[start:token.i]:
        if t.text.lower().rstrip(".") in NEGATORS or t.dep_ == "neg":
            return True
    return False


def extract_absa(doc):
    """Returns list of {aspect, descriptor, sentiment} dicts."""
    results = []

    # noun chunk map (same as V1)
    chunk_map = {}
    for chunk in doc.noun_chunks:
        for token in chunk:
            if token.pos_ in {"NOUN", "PROPN"}:
                chunk_map[token.i] = chunk.text.lower()

    def aspect_of(token):
        return chunk_map.get(token.i if hasattr(token, "i") else token.head.i,
                             token.text.lower())

    def add(aspect, descriptor, token):
        negated = _has_negation_window(token)
        sentiment = _classify(descriptor, negated)
        # dedup: one entry per (aspect) — keep first
        if not any(r["aspect"] == aspect for r in results):
            results.append({
                "aspect": aspect,
                "descriptor": descriptor,
                "sentiment": sentiment,
            })

    for token in doc:
        if token.is_punct or token.text == "-" or token.is_space:
            continue
        head = token.head

        # P1: amod -> noun (V1)
        if token.dep_ == "amod" and head.pos_ in {"NOUN", "PROPN"}:
            add(aspect_of(head), token.text.lower(), token)

        # P2: acomp -> AUX/VERB with nsubj (V1)
        elif token.dep_ == "acomp" and head.pos_ in {"AUX", "VERB"}:
            subj = next((w for w in head.children if w.dep_ in {"nsubj", "nsubjpass"}), None)
            if subj and subj.pos_ in {"NOUN", "PROPN"}:
                add(aspect_of(subj), token.text.lower(), token)

        # P3: VBN + auxpass (V1)
        elif token.tag_ == "VBN" and any(c.dep_ in {"auxpass", "aux:pass"} for c in token.children):
            subj = next((w for w in token.children if w.dep_ in {"nsubjpass"}), None)
            if subj and subj.pos_ in {"NOUN", "PROPN"}:
                add(aspect_of(subj), token.text.lower(), token)

        # P4: compound noun as subject with cop + acomp (NEW)
        # e.g. "delivery driver was rude" -> aspect="delivery driver", descriptor="rude"
        elif token.dep_ == "compound" and head.dep_ == "nsubj" and head.pos_ in {"NOUN", "PROPN"}:
            root_verb = head.head
            if root_verb.pos_ in {"AUX", "VERB"}:
                acomp = next((c for c in root_verb.children if c.dep_ == "acomp"), None)
                if acomp:
                    compound_aspect = chunk_map.get(head.i, f"{token.text} {head.text}").lower()
                    add(compound_aspect, acomp.text.lower(), acomp)

        # P5: relative clause (NEW): "box that arrived damaged"
        elif token.dep_ == "relcl":
            acomp = next((c for c in token.children if c.dep_ == "acomp"), None)
            if acomp:
                add(aspect_of(token), acomp.text.lower(), acomp)
            else:
                amod = next((c for c in token.children if c.dep_ == "amod"), None)
                if amod:
                    add(aspect_of(token), amod.text.lower(), amod)

    # P6: verbal predicate sentiment (NEW - OOD robustness)
    # Covers verb-resultative ("hinge snapped"), event verbs ("zipper jammed",
    # "antifreeze leaked", "grille gleams"), xcomp+advmod, and oprd resultatives.
    for token in doc:
        if token.is_punct or token.text == "-" or token.is_space:
            continue
        lemma = token.lemma_.lower()
        verb_pol = _verb_polarity(lemma)
        is_predicate_token = token.pos_ in {"VERB", "AUX", "NOUN", "PROPN"} and \
            token.pos_ not in {"ADJ", "ADV", "ADP", "DET"}
        # candidate aspect(s): the verb's nsubj/object and/or the noun it predicates on
        aspect_cands = []
        for ch in token.children:
            if ch.dep_ in {"nsubj", "nsubjpass", "oprd", "acl", "relcl", "pobj", "compound"} and ch.pos_ in {"NOUN", "PROPN"}:
                aspect_cands.append(aspect_of(ch))
        if token.pos_ == "NOUN" and token.head.dep_ in {"acl", "relcl"} and token.dep_ == "nsubj":
            aspect_cands.append(aspect_of(token))
        # for reduced-clause defect/event verbs ("leaked" under noun "antifreeze"),
        # the verb's head noun is the aspect
        if token.pos_ == "VERB" and token.head.pos_ in {"NOUN", "PROPN"} and token.dep_ in {"acl", "relcl"}:
            aspect_cands.append(aspect_of(token.head))

        if verb_pol and is_predicate_token and aspect_cands:
            negated = _has_negation_window(token)
            sentiment = "Negative" if verb_pol == "Negative" else "Positive"
            if negated:
                sentiment = "Negative" if sentiment == "Positive" else "Positive"
            for asp in aspect_cands:
                if not any(r["aspect"] == asp for r in results):
                    results.append({
                        "aspect": asp,
                        "descriptor": lemma,
                        "sentiment": sentiment,
                    })
            continue

        # P7: xcomp/advmod quality signal on a verb with no dedicated verb polarity
        # e.g. "absorbs spills beautifully", "shut properly"
        for ch in token.children:
            if ch.dep_ == "xcomp" and token.lemma_ in {"absorb", "hold", "cradle", "cushion",
                                                       "seal", "fit", "support", "work", "function"}:
                adv = next((a for a in ch.children if a.dep_ == "advmod" and a.pos_ == "ADV"), None)
                subj = next((s for s in token.children if s.dep_ in {"nsubj", "nsubjpass"}), None)
                if adv and subj and subj.pos_ in {"NOUN", "PROPN"}:
                    add(aspect_of(subj), adv.text.lower(), adv)
        # oprd resultative: "hinge snapped clean in two"
        if any(c.dep_ == "oprd" for c in token.children):
            oprd = next(c for c in token.children if c.dep_ == "oprd")
            subj = next((s for s in token.children if s.dep_ in {"nsubj", "nsubjpass"}), None)
            if subj and subj.pos_ in {"NOUN", "PROPN"}:
                add(aspect_of(subj), oprd.text.lower(), oprd)

    return results