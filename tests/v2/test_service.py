"""Integration test for V2AnalysisService end-to-end."""
import pytest
from mdas.v2 import V2AnalysisService


@pytest.fixture(scope="module")
def service():
    return V2AnalysisService()


class TestV2Service:
    def test_analyze_passive(self, service):
        r = service.analyze("The package was delivered by the courier.", "test-1")
        assert r.status == "success"
        assert r.linguistics.voice.summary_label == "passive"
        assert r.spam.label in ("spam", "ham", "needs_human_triage")

    def test_analyze_spam(self, service):
        r = service.analyze("URGENT: your account has been suspended. Reply now.", "test-2")
        assert r.status == "success"
        assert r.radar.urgency > 0

    def test_analyze_empty_rejected(self, service):
        with pytest.raises(ValueError):
            service.analyze("", "test-3")

    def test_analyze_non_english(self, service):
        r = service.analyze("Bonjour le monde", "test-4")
        assert hasattr(r, "status") and r.status == "unsupported_language"

    def test_analyze_v2_engine(self, service):
        r = service.analyze("The box arrived smashed.", "test-5")
        assert r.spam.method == "tfidf_linear_svc_v2"

    def test_analyze_has_absa(self, service):
        r = service.analyze("The box arrived completely smashed.", "test-6")
        assert isinstance(r.absa, list)

    def test_analyze_has_radar(self, service):
        r = service.analyze("Cancel my subscription immediately.", "test-7")
        assert r.radar.churn_risk >= 0
        assert r.radar.urgency >= 0
