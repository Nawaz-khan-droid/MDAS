"""MDAS V2 — upgraded analysis engine (drop-in replacement for V1).

Reuses V1's API contract (AnalysisResponse), spaCy backend, voice rules,
entity extraction, and VADER sentiment. Swaps in improved:
  - ABSA      : mdas.v2.absa      (verb-predicate + adjective patterns, lexicon)
  - Radar     : mdas.v2.signals   (negation-aware, phrase weighting, strong triggers)
  - Spam      : mdas.v2.spam      (margin-triage LinearSVC on 7,699 samples)
"""
from mdas.v2.service import V2AnalysisService

__all__ = ["V2AnalysisService"]
