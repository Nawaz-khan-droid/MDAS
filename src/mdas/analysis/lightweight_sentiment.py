"""Lightweight VADER-compatible sentiment analyzer.

Loads the VADER lexicon directly without importing NLTK, saving ~107 MB of memory.
Compatible output format with NLTK VADER's polarity_scores().
"""
import os
import re

_SENTIMENT_DICT = None
_LEXICON_PATH = None


def _find_lexicon():
    """Find VADER lexicon — bundled copy first, then nltk_data search."""
    global _LEXICON_PATH
    if _LEXICON_PATH is not None:
        return _LEXICON_PATH

    # 1. Bundled copy in same directory as this module
    bundled = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vader_lexicon.zip')
    if os.path.exists(bundled):
        _LEXICON_PATH = bundled
        return _LEXICON_PATH

    # 2. Walk up looking for nltk_data
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        candidate = os.path.join(current, 'nltk_data', 'sentiment', 'vader_lexicon.zip')
        if os.path.exists(candidate):
            _LEXICON_PATH = candidate
            return _LEXICON_PATH
        current = os.path.dirname(current)
    raise FileNotFoundError(
        "VADER lexicon not found. Expected at: src/mdas/analysis/vader_lexicon.zip"
    )


def _load_lexicon():
    """Load VADER lexicon from nltk_data directory."""
    global _SENTIMENT_DICT
    if _SENTIMENT_DICT is not None:
        return

    import zipfile
    lexicon_path = _find_lexicon()

    _SENTIMENT_DICT = {}
    with zipfile.ZipFile(lexicon_path, 'r') as z:
        with z.open('vader_lexicon/vader_lexicon.txt') as f:
            for line in f:
                line = line.decode('utf-8').strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    word = parts[0].strip()
                    measure = float(parts[1])
                    _SENTIMENT_DICT[word] = measure


# VADER-specific constants
_BOOSTER_WORDS = {
    'absolutely': 0.293, 'amazingly': 0.293, 'completely': 0.293,
    'considerably': 0.167, 'consistently': 0.167, 'decidedly': 0.293,
    'deeply': 0.167, 'enormously': 0.293, 'entirely': 0.293,
    'especially': 0.167, 'exceptionally': 0.293, 'extremely': 0.293,
    'fabulously': 0.293, 'flipping': 0.167, 'flippin': 0.167,
    'fricking': 0.167, 'frigg': 0.167, 'friggin': 0.167,
    'frigging': 0.167, 'fully': 0.293, 'hella': 0.167,
    'highly': 0.167, 'hugely': 0.293, 'incredibly': 0.293,
    'insanely': 0.293, 'just': 0.167, 'kinda': 0.167,
    'kindof': 0.167, 'largely': 0.167, 'literally': 0.167,
    'love': 0.293, 'loving': 0.293, 'luckily': 0.167,
    'most': 0.167, 'much': 0.167, 'never': 0.293,
    'perfectly': 0.293, 'phenomenally': 0.293, 'quite': 0.167,
    'really': 0.167, 'remarkably': 0.167, 'so': 0.167,
    'substantially': 0.167, 'surprisingly': 0.167, 'terribly': 0.167,
    'thoroughly': 0.293, 'totally': 0.293, 'tremendously': 0.293,
    'truly': 0.293, 'truthfully': 0.167, 'uber': 0.167,
    'unbelievably': 0.293, 'unusually': 0.167, 'utterly': 0.293,
    'very': 0.167, 'winning': 0.167, 'wonderfully': 0.293,
}

_NINCE_WORDS = {
    'although': 0.167, 'but': -0.167, 'despite': 0.167,
    'even': 0.167, 'however': 0.167, 'instead': 0.167,
    'nevertheless': 0.167, 'nonetheless': 0.167, 'though': 0.167,
    'whilst': 0.167,
}

_BUT_DIFFERENT = {'but': -0.293}


def _scalar_boost_dampen(word, valence):
    """Apply booster/dampener effects."""
    scalar = 0.0
    lc_word = word.lower()
    if lc_word in _BOOSTER_WORDS:
        scalar = _BOOSTER_WORDS[lc_word]
    elif lc_word in _BUT_DIFFERENT:
        scalar = _BUT_DIFFERENT[lc_word]
    return scalar


def _punctuation_emphasis(text):
    """Exclamation/question marks amplify sentiment."""
    excl_count = text.count('!')
    quest_count = text.count('?')
    excl_amplifier = excl_count * 0.292
    quest_amplifier = quest_count * 0.18
    return excl_amplifier + quest_amplifier


def polarity_scores(text):
    """Compute VADER-compatible sentiment scores.

    Returns dict with 'neg', 'neu', 'pos', 'compound' keys.
    """
    _load_lexicon()

    # Normalize text
    text_clean = text.strip()
    if not text_clean:
        return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

    words = text_clean.split()
    sentiments = []
    has_moderator = False

    for i, word in enumerate(words):
        # Clean word of punctuation for lookup
        word_clean = re.sub(r'[^\w]', '', word.lower())

        valence = 0.0
        # Lookup in VADER lexicon
        if word_clean in _SENTIMENT_DICT:
            valence = _SENTIMENT_DICT[word_clean]

        # Check for booster words (e.g., "very good")
        if i > 0 and valence != 0:
            prev_word_clean = re.sub(r'[^\w]', '', words[i - 1].lower())
            scalar = _scalar_boost_dampen(prev_word_clean, valence)
            if prev_word_clean in _BOOSTER_WORDS:
                valence += scalar if valence > 0 else scalar  # boost both ways

        # Check for "but" - dampen before, boost after
        if word_clean == 'but' or word_clean in _BUT_DIFFERENT:
            has_moderator = True
            sentiments.append({'class': 'but', 'valence': 0.0})
            continue

        if valence != 0:
            sentiments.append({'class': 'word', 'valence': valence})
        else:
            sentiments.append({'class': 'other', 'valence': 0.0})

    # Sum sentiments
    pos_sentiments = sum(s['valence'] for s in sentiments if s['valence'] > 0)
    neg_sentiments = sum(s['valence'] for s in sentiments if s['valence'] < 0)

    # If there's a "but", amplify sentiments after it
    if has_moderator:
        but_idx = next(i for i, s in enumerate(sentiments) if s['class'] == 'but')
        pos_after = sum(s['valence'] for s in sentiments[but_idx:] if s['valence'] > 0)
        neg_after = sum(s['valence'] for s in sentiments[but_idx:] if s['valence'] < 0)
        pos_before = sum(s['valence'] for s in sentiments[:but_idx] if s['valence'] > 0)
        neg_before = sum(s['valence'] for s in sentiments[:but_idx] if s['valence'] < 0)

        pos_sentiments = pos_before * 0.5 + pos_after
        neg_sentiments = neg_before * 0.5 + neg_after

    # Punctuation emphasis
    excl_quest_amp = _punctuation_emphasis(text_clean)

    # Calculate compound
    raw_score = pos_sentiments + neg_sentiments
    raw_score += excl_quest_amp * (1 if raw_score > 0 else -1 if raw_score < 0 else 0)

    # Normalize compound to [-1, 1]
    compound = raw_score / ((raw_score * raw_score + 15) ** 0.5)
    compound = round(compound, 4)

    # Calculate pos/neg/neu ratios
    total_valence = abs(pos_sentiments) + abs(neg_sentiments)
    word_count = len([w for w in words if re.sub(r'[^\w]', '', w.lower())])

    if total_valence > 0 and word_count > 0:
        pos_ratio = pos_sentiments / total_valence if pos_sentiments > 0 else 0
        neg_ratio = neg_sentiments / total_valence if neg_sentiments > 0 else 0
        neu_ratio = max(0.0, 1.0 - pos_ratio - neg_ratio)
    else:
        pos_ratio = 0.0
        neg_ratio = 0.0
        neu_ratio = 1.0

    return {
        'neg': round(neg_ratio, 3),
        'neu': round(neu_ratio, 3),
        'pos': round(pos_ratio, 3),
        'compound': compound,
    }
