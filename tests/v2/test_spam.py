"""Tests for mdas.v2.spam — V2 spam classifier."""
import pytest
from pathlib import Path
from mdas.v2.spam import SpamModelV2, _verify_model_hash, DEFAULT_MODEL, DEFAULT_META


class TestModelHash:
    def test_valid_hash_passes(self):
        meta = __import__("json").loads(DEFAULT_META.read_text(encoding="utf-8"))
        assert _verify_model_hash(DEFAULT_MODEL, meta["model_sha256_prefix"])

    def test_invalid_hash_fails(self):
        assert not _verify_model_hash(DEFAULT_MODEL, "0000000000000000")

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            SpamModelV2(path=Path("/nonexistent/joblib"))


class TestSpamModelV2:
    @pytest.fixture
    def model(self):
        return SpamModelV2()

    def test_version(self, model):
        assert model.version() == "2.0"

    def test_spam_detected(self, model):
        label, margin = model.classify("Win a free trip now! Text ORDER to 8090.")
        assert label == "spam"
        assert margin > 0

    def test_ham_detected(self, model):
        label, margin = model.classify("The package was delivered yesterday.")
        assert label == "ham"
        assert margin < 0

    def test_triage_zone(self, model):
        label, margin = model.classify("Please cancel my subscription immediately.")
        assert label in ("spam", "ham", "needs_human_triage")

    def test_is_spam(self, model):
        assert model.is_spam("Win a free trip now!")
        assert not model.is_spam("The package was delivered.")

    def test_hard_label(self, model):
        assert model.hard_label("Win a free trip now!") in ("spam", "ham")

    def test_trace(self, model):
        t = model.trace()
        assert t["model"] == "spam_v2"
        assert "sha256" in t
        assert t["sha256"] == "eddf0d6415596903"
