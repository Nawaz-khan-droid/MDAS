from collections import Counter

def analyze_statistics(doc):
    tokens = [t for t in doc if not t.is_space]
    lexical = [t for t in tokens if not t.is_punct]
    words = [t.text for t in lexical if t.is_alpha or t.like_num]
    alpha = [t.text.lower() for t in lexical if t.is_alpha]
    sentences = list(doc.sents)
    return {
        "characters": len(doc.text),
        "words": len(words),
        "alphabetic_words": len(alpha),
        "sentences": len(sentences),
        "tokens": len(tokens),
        "unique_words": len(set(alpha)),
        "average_words_per_sentence": round(len(words)/len(sentences), 3) if sentences else 0.0,
        "lexical_diversity": round(len(set(alpha))/len(alpha), 3) if alpha else 0.0,
        "punctuation_marks": sum(1 for t in tokens if t.is_punct),
        "numbers": sum(1 for t in lexical if t.like_num),
    }
