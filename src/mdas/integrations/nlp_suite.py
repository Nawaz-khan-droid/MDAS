"""Explicit boundary for optional NLP Suite-aligned processing.

NLP Suite is treated as an application rather than as a stable Python API.
The supported reuse path is its underlying NLP stack, especially Stanza.
If a future decision is made to vendor a specific NLP Suite source module,
put that implementation here and pin its exact version/license.
"""
from mdas.nlp.stanza_backend import StanzaBackend

def build_nlp_suite_aligned_backend():
    return StanzaBackend()
