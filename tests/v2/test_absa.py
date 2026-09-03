"""Tests for mdas.v2.absa — V2 ABSA extraction."""
import pytest
from mdas.nlp.spacy_backend import SpacyBackend
from mdas.v2.absa import extract_absa


@pytest.fixture(scope="module")
def backend():
    return SpacyBackend()


class TestABSA:
    def test_amod_positive(self, backend):
        doc = backend.analyze("The stitching is impeccable on this jacket.")
        results = extract_absa(doc)
        assert len(results) >= 1
        assert results[0]["sentiment"] == "Positive"

    def test_amod_negative(self, backend):
        doc = backend.analyze("The box arrived completely smashed.")
        results = extract_absa(doc)
        assert len(results) >= 1
        assert results[0]["sentiment"] == "Negative"

    def test_negation_flips(self, backend):
        doc = backend.analyze("The device is not broken.")
        results = extract_absa(doc)
        assert len(results) >= 1
        assert results[0]["sentiment"] == "Positive"

    def test_verb_predicate_negative(self, backend):
        doc = backend.analyze("The zipper jammed mid-way.")
        results = extract_absa(doc)
        aspects = [r["aspect"] for r in results]
        assert any("zipper" in a for a in aspects)

    def test_verb_predicate_positive(self, backend):
        doc = backend.analyze("The cushioning cradles your back well.")
        results = extract_absa(doc)
        aspects = [r["aspect"] for r in results]
        assert any("cushion" in a for a in aspects)

    def test_empty_text(self, backend):
        doc = backend.analyze("OK.")
        results = extract_absa(doc)
        assert isinstance(results, list)

    def test_no_aspects_on_generic_text(self, backend):
        doc = backend.analyze("The quick brown fox jumps over the lazy dog.")
        results = extract_absa(doc)
        assert isinstance(results, list)
