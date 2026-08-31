import pytest
import uuid
from unittest.mock import patch, MagicMock
from mdas.application.analysis_service import AnalysisService
from mdas.api.schemas import UnsupportedLanguageResponse

def test_unsupported_language_prevents_nlp_execution():
    service = AnalysisService()
    
    # Spy on the NLP backend and ML registry
    with patch.object(service.backend, "analyze", wraps=service.backend.analyze) as mock_spacy_analyze, \
         patch.object(service.registry, "predict", wraps=service.registry.predict) as mock_registry_predict, \
         patch.object(service.sia, "polarity_scores", wraps=service.sia.polarity_scores) as mock_vader:
         
         result = service.analyze("Hola, este producto es muy bueno y me gusta.", str(uuid.uuid4()))
         
         assert isinstance(result, UnsupportedLanguageResponse)
         
         # PROOF: Inference methods were NEVER called
         mock_spacy_analyze.assert_not_called()
         mock_registry_predict.assert_not_called()
         mock_vader.assert_not_called()
