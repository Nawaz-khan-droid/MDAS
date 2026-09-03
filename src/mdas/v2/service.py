"""V2 analysis service — mirrors V1 AnalysisService but uses V2 modules.

V1 code (deployed) is NOT modified. This service produces the SAME
AnalysisResponse shape as V1, but swaps in:
  - ABSA      : mdas.v2.absa       (P4 compound, P5 relcl, P6 verb-predicate, lexicon)
  - Radar     : mdas.v2.signals    (negation window, phrase weighting, strong triggers)
  - Spam      : mdas.v2.spam       (margin triage on 7,699 labeled samples)

Unchanged, reused from V1: language detection, statistics, linguistics/voice,
entities, sentiment (VADER). Voice is rule-based and version-independent.
"""
from typing import Union
from pathlib import Path

from mdas.api.schemas import (
    AnalysisResponse, LanguageResult, StatisticsResult, LinguisticsResult, VoiceResult,
    EntityResult, ClassificationResult, SentimentResult, AspectResult, RadarSignals,
    UnsupportedLanguageResponse,
)
from mdas.application.analysis_service import AnalysisService as V1AnalysisService
from mdas.nlp.spacy_backend import SpacyBackend
from mdas.analysis.language import detect_language
from mdas.analysis.linguistics import analyze_linguistics
from mdas.core.constants import MAX_TEXT_LENGTH
from mdas.analysis.lightweight_sentiment import polarity_scores as vader_polarity_scores
from mdas.v2.absa import extract_absa as v2_extract_absa
from mdas.v2.signals import build_signals as v2_signals
from mdas.v2.spam import SpamModelV2


class V2AnalysisService(V1AnalysisService):
    """V2 engine: same interface as V1 AnalysisService, V2 internals for improved features."""

    def __init__(self, model_dir="models", allowed_tasks=None, v2_model_path=None):
        if allowed_tasks is None:
            allowed_tasks = ["spam"]
        self.backend = SpacyBackend()
        self.registry = None  # V2 uses its own spam model, not V1 registry

        self._extract_absa = v2_extract_absa
        self._signals = v2_signals
        if v2_model_path is None:
            v2_model_path = str(Path(__file__).resolve().parent / "models" / "spam_v2.joblib")
        self._spam = SpamModelV2(v2_model_path)

    def analyze(self, text: str, analysis_id: str) -> Union[AnalysisResponse, UnsupportedLanguageResponse]:
        # 1. INPUT VALIDATION
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError(f"Text length ({len(text)}) exceeds maximum allowed ({MAX_TEXT_LENGTH} chars).")

        # 2. LANGUAGE DETECTION + gate (same as V1)
        lang_detected = detect_language(text)
        language_res = LanguageResult(
            code=lang_detected.get("language", "unknown"),
            label=lang_detected.get("label", "Unknown"),
            confidence=lang_detected.get("score"),
            method=lang_detected.get("method", "langdetect"),
        )
        if language_res.code != "en":
            return UnsupportedLanguageResponse(language=language_res, message="MDAS V2 currently supports English text.")

        # 4. NLP
        doc = self.backend.analyze(text)

        # 5. STATISTICS (same as V1)
        word_count = len([t for t in doc if not t.is_punct and not t.is_space])
        char_count = len(text)
        sent_count = len(list(doc.sents))
        token_count = len(doc)
        paragraphs = len([p for p in text.split("\n\n") if p.strip()])
        minutes = word_count / 200.0
        if minutes < 1.0:
            reading_time = "< 1 min"
        elif minutes < 60.0:
            reading_time = f"~{int(round(minutes))} min"
        else:
            hours = int(minutes // 60)
            mins = int(round(minutes % 60))
            reading_time = f"~{hours} hr {mins} min"
        stats_res = StatisticsResult(
            words=word_count, characters=char_count, sentences=sent_count,
            tokens=token_count, paragraphs=paragraphs, reading_time=reading_time,
        )

        # 6. LINGUISTICS + VOICE (V1 rules, unchanged) + NER
        ling_raw = analyze_linguistics(doc, include_token_details=False)
        voice_raw = ling_raw.get("voice", {})
        voice_segments = []
        for s in voice_raw.get("segments", []):
            label = s.get("voice", "unknown").lower()
            ev_raw = s.get("evidence", {})
            if isinstance(ev_raw, str):
                evidence_obj = {"text": ev_raw}
            else:
                evidence_obj = ev_raw
            voice_segments.append({"text": s["text"], "label": label, "evidence": evidence_obj})
        counts = voice_raw.get("summary", {})
        active = counts.get("active", 0)
        passive = counts.get("passive", 0)
        linking = counts.get("linking", 0)
        if active > 0 and passive == 0 and linking == 0:
            summary_label = "active"
        elif passive > 0 and active == 0 and linking == 0:
            summary_label = "passive"
        elif linking > 0 and active == 0 and passive == 0:
            summary_label = "linking"
        elif active == 0 and passive == 0 and linking == 0:
            summary_label = "unknown"
        else:
            summary_label = "mixed"
        voice_res = VoiceResult(summary_label=summary_label, method="dependency_rules", sentences=voice_segments)

        mapped_entities = []
        extracted_spans = set()
        for ent in doc.ents:
            label = ent.label_
            text_lower = ent.text.lower()
            if text_lower in {"adidas", "nike", "puma", "microsoft", "apple", "google"}:
                label = "ORG"
            elif label in {"GPE", "LOC"}:
                label = "LOCATION"
            elif text_lower in {"today", "tomorrow", "yesterday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}:
                label = "DATE"
            elif label in {"FAC", "LAW", "WORK_OF_ART"}:
                label = "PRODUCT"
            if label not in {"ORG", "LOCATION", "DATE", "PRODUCT", "PERSON", "TIME", "MONEY"}:
                continue
            if label == "DATE" and text_lower in {"monthly", "daily", "weekly", "yearly", "annually"}:
                continue
            mapped_entities.append(EntityResult(text=ent.text, label=label))
            extracted_spans.add(text_lower)
        ling_res = LinguisticsResult(voice=voice_res, entities=mapped_entities)

        # 7. SENTIMENT (VADER, same as V1)
        scores = vader_polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            sent_label = "positive"
        elif compound <= -0.05:
            sent_label = "negative"
        else:
            sent_label = "neutral"
        sent_res = SentimentResult(label=sent_label, score=compound, method="lexicon_rules")

        # 8. SPAM (V2 margin-triage model)
        spam_label_v2, margin_v2 = self._spam.classify(text)
        # Map triage -> the label the API exposes; keep confidence as margin magnitude
        spam_res = ClassificationResult(
            label=str(spam_label_v2),
            confidence=float(abs(margin_v2)) if margin_v2 is not None else 0.0,
            method="tfidf_linear_svc_v2",
            model_version=self._spam.version(),
            candidates=[],
        )

        # 9. ABSA (V2)
        absa_raw = self._extract_absa(doc)
        absa_res = [AspectResult(**a) for a in absa_raw]

        # 10. RADAR (V2)
        raw_signals = self._signals(text, sent_label)
        radar_res = RadarSignals(
            sentiment=(compound + 1) / 2.0,
            urgency=raw_signals["urgency"]["score"],
            churn_risk=raw_signals["churn_risk"]["score"],
            sarcasm=raw_signals["sarcasm"]["score"],
            toxicity=raw_signals["toxicity"]["score"],
        )

        return AnalysisResponse(
            analysis_id=analysis_id, status="success", language=language_res,
            statistics=stats_res, linguistics=ling_res, sentiment=sent_res,
            spam=spam_res, absa=absa_res, radar=radar_res,
        )