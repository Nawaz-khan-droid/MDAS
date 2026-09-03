"""Tests for mdas.v2.signals — V2 radar signals."""
import pytest
from mdas.v2.signals import build_signals, urgency_signal, churn_signal, toxicity_signal


class TestRadarSignals:
    def test_urgency_high(self):
        r = urgency_signal("URGENT: respond immediately or lose access.")
        assert r["label"] == "high"

    def test_urgency_low(self):
        r = urgency_signal("No rush, whenever you get around to it.")
        assert r["label"] == "low"

    def test_churn_high(self):
        r = churn_signal("I am leaving to switch to a competitor.")
        assert r["label"] == "high"

    def test_churn_low(self):
        r = churn_signal("I intend to renew for another year.")
        assert r["label"] == "low"

    def test_toxicity_high(self):
        r = toxicity_signal("You are an idiot and your service is garbage.")
        assert r["label"] == "high"

    def test_toxicity_low(self):
        r = toxicity_signal("Thank you for your prompt professionalism.")
        assert r["label"] == "low"

    def test_build_signals_returns_all_keys(self):
        r = build_signals("Hello world", "neutral")
        assert "urgency" in r
        assert "churn_risk" in r
        assert "toxicity" in r
        assert "sarcasm" in r
        assert "sentiment_source" in r
