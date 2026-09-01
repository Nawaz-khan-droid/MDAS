import pytest
import uuid
from mdas.application.analysis_service import AnalysisService
from mdas.api.schemas import UnsupportedLanguageResponse, AnalysisResponse

def test_empty_input_rejected():
    service = AnalysisService()
    with pytest.raises(ValueError, match="Input text cannot be empty."):
        service.analyze("   ", str(uuid.uuid4()))

def test_unsupported_language_gate():
    service = AnalysisService()
    # Spanish text >100 chars to bypass heuristic_short_text override
    result = service.analyze("Este es un producto muy malo que no funciona nada bien, necesito devolverlo cuanto antes porque estoy muy molesto con el servicio al cliente.", str(uuid.uuid4()))
    
    assert isinstance(result, UnsupportedLanguageResponse)
    assert result.status == "unsupported_language"
    assert result.language.code == "es" # langdetect detects Spanish
    assert result.message == "MDAS V1 currently supports English text."

def test_english_proceeds():
    service = AnalysisService()
    result = service.analyze("The customer service was absolutely terrible and I want a refund.", str(uuid.uuid4()))
    
    assert isinstance(result, AnalysisResponse)
    assert result.language.code == "en"
    assert result.status == "success"
    # Verify NLP ran
    assert result.statistics.words > 0
    assert result.linguistics.voice.summary_label in ["active", "passive", "mixed", "unknown"]
    assert hasattr(result, "spam") and result.spam.label is not None
