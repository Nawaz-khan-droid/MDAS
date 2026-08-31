import langdetect
from langdetect.lang_detect_exception import LangDetectException

def detect_language(text: str) -> dict:
    """
    Real language detection using `langdetect`.
    Returns a dict with 'language' code, 'score', and 'method'.
    """
    # Quick fast-fail for empty or whitespace-only text
    if not text or not text.strip():
        return {
            "language": "unknown",
            "label": "Unknown",
            "score": 0.0,
            "method": "langdetect"
        }
        
    try:
        # Get the most probable language
        detected = langdetect.detect_langs(text)[0]
        lang_code = detected.lang
        prob = detected.prob
        
        # Simple mapping for common labels (can be expanded)
        labels = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "hi": "Hindi",
            "da": "Danish"
        }
        
        return {
            "language": lang_code,
            "label": labels.get(lang_code, lang_code.upper()),
            "score": round(prob, 3),
            "method": "langdetect"
        }
    except LangDetectException:
        # Usually happens if there are no alphabetical features (e.g., only numbers/punctuation)
        return {
            "language": "unknown",
            "label": "Unknown",
            "score": 0.0,
            "method": "langdetect"
        }

identify_english = detect_language
