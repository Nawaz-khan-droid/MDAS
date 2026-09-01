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
        
        # langdetect often misclassifies short, typo-ridden English (e.g., as Welsh 'cy' or Somali 'so')
        # If it detects non-English for a short text, check if it contains basic English words.
        if lang_code != "en" and len(text.strip()) < 100:
            common_english = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", 
                              "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", 
                              "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", 
                              "an", "will", "my", "one", "all", "would", "there", "their", "what", 
                              "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
                              "hey", "hi", "hello", "yes", "no", "ok", "okay", "please", "thanks", "can"}
            
            # Simple tokenization by splitting on non-alphabetic
            import re
            words = set(re.findall(r'[a-z]+', text.lower()))
            if words.intersection(common_english):
                lang_code = "en"
                prob = 1.0
                method = "heuristic_short_text"
            else:
                method = "langdetect"
        else:
            method = "langdetect"
        
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
            "method": method
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
