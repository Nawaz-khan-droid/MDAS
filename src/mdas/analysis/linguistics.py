from collections import Counter
from mdas.analysis.entities import extract_entities
from mdas.analysis.voice import analyze_voice

def analyze_linguistics(doc, include_token_details=True):
    entities = extract_entities(doc)
    pos = Counter(); deps = Counter(); lemmas = Counter(); tokens = []
    for token in doc:
        if token.is_space: continue
        pos[token.pos_] += 1
        deps[token.dep_] += 1
        if token.lemma_: lemmas[token.lemma_.lower()] += 1
        if include_token_details:
            tokens.append({
                "text": token.text, "lemma": token.lemma_, "pos": token.pos_,
                "tag": token.tag_, "dependency": token.dep_, "head": token.head.text,
                "is_stop": bool(token.is_stop), "is_punct": bool(token.is_punct)
            })
    return {
        "entities": [e.__dict__ for e in entities],
        "pos_counts": dict(pos),
        "dependency_counts": dict(deps),
        "top_lemmas": [{"lemma": x, "count": n} for x,n in lemmas.most_common(25)],
        "voice": analyze_voice(doc),
        "tokens": tokens if include_token_details else None,
        "sentence_count": len(list(doc.sents)),
    }
