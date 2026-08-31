from typing import Union
from mdas.api.schemas import (
    AnalysisResponse, LanguageResult, StatisticsResult, LinguisticsResult, VoiceResult,
    EntityResult, ClassificationResult, SentimentResult,
    UnsupportedLanguageResponse, AspectResult, UrgencyResult, ChurnResult
)
from mdas.classification.registry import ModelRegistry
from mdas.nlp.spacy_backend import SpacyBackend
from mdas.analysis.language import detect_language
from mdas.analysis.statistics import analyze_statistics
from mdas.analysis.linguistics import analyze_linguistics
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class AnalysisService:
    def __init__(self, model_dir="models"):
        # Note: Models are initialized here at startup, as required for single-server performance.
        # The language gate prevents *execution* of these models on unsupported text.
        self.backend = SpacyBackend()
        self.registry = ModelRegistry(model_dir)
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, text: str, analysis_id: str) -> Union[AnalysisResponse, UnsupportedLanguageResponse]:
        # 1. INPUT VALIDATION
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        # 2. LANGUAGE DETECTION
        lang_detected = detect_language(text)
        language_res = LanguageResult(
            code=lang_detected.get("language", "unknown"),
            label=lang_detected.get("label", "Unknown"),
            confidence=lang_detected.get("score"),
            method=lang_detected.get("method", "langdetect")
        )

        # 3. LANGUAGE SUPPORT GATE
        if language_res.code != "en":
            return UnsupportedLanguageResponse(
                language=language_res,
                message="MDAS V1 currently supports English text."
            )

        # 4. TEXT PREPROCESSING / LANGUAGE-AWARE NLP INITIALIZATION
        doc = self.backend.analyze(text)

        # 5. STATISTICS
        word_count = len([t for t in doc if not t.is_punct and not t.is_space])
        char_count = len(text)
        sent_count = len(list(doc.sents))
        token_count = len(doc)
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
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
            words=word_count,
            characters=char_count,
            sentences=sent_count,
            tokens=token_count,
            paragraphs=paragraphs,
            reading_time=reading_time
        )

        # 6. LINGUISTIC ANALYSIS & NER
        ling_raw = analyze_linguistics(doc, include_token_details=False)
        voice_raw = ling_raw.get("voice", {})
        
        # Determine dominant voice from summary counts
        voice_segments = []
        for s in voice_raw.get("segments", []):
            label = s.get("voice", "unknown").lower()
            ev_raw = s.get("evidence", {})
            if isinstance(ev_raw, str):
                # Fallback if old code somehow runs
                evidence_obj = {"text": ev_raw}
            else:
                evidence_obj = ev_raw
                
            voice_segments.append({
                "text": s["text"],
                "label": label,
                "evidence": evidence_obj
            })
            
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

        voice_res = VoiceResult(
            summary_label=summary_label,
            method="dependency_rules",
            sentences=voice_segments
        )
        
        # Filter and map entities to strict ontology
        mapped_entities = []
        extracted_spans = set()
        
        for ent in doc.ents:
            label = ent.label_
            text_lower = ent.text.lower()
            
            # Domain normalization
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
                
            # filter out false dates like 'monthly', 'daily'
            if label == "DATE" and text_lower in {"monthly", "daily", "weekly", "yearly", "annually"}:
                continue
            
            mapped_entities.append(EntityResult(text=ent.text, label=label))
            extracted_spans.add(text_lower)
            
        # Fallback explicit keyword extractor for MVP domains
        for t in doc:
            t_lower = t.text.lower()
            if t_lower in {"adidas", "nike", "puma", "microsoft", "apple", "google"} and t_lower not in extracted_spans:
                mapped_entities.append(EntityResult(text=t.text, label="ORG"))
                extracted_spans.add(t_lower)
            elif t_lower in {"today", "tomorrow", "yesterday"} and t_lower not in extracted_spans:
                mapped_entities.append(EntityResult(text=t.text, label="DATE"))
                extracted_spans.add(t_lower)
        
        ling_res = LinguisticsResult(voice=voice_res, entities=mapped_entities)

        # 7. SENTIMENT (VADER)
        scores = self.sia.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            sent_label = "positive"
        elif compound <= -0.05:
            sent_label = "negative"
        else:
            sent_label = "neutral"
            
        sent_res = SentimentResult(
            label=sent_label,
            score=compound,
            method="vader"
        )
        
        # 8. CLASSIFICATION (Spam & Intent)
        def predict_task(task_name):
            if self.registry.has(task_name):
                try:
                    r = self.registry.predict(task_name, text)
                    if r.status == "ok" and r.label:
                        return ClassificationResult(
                            label=r.label,
                            confidence=r.confidence or 0.0,
                            method=r.method if hasattr(r, "method") and r.method else "legacy_model",
                            model_version=r.model_version if hasattr(r, "model_version") and r.model_version else "v1"
                        )
                except Exception as e:
                    import logging
                    logging.error(f"Classification failed for {task_name}: {e}")
                    pass
            return ClassificationResult(label="unknown", confidence=0.0, method="missing_model", model_version="unknown")

        spam_res = predict_task("spam")
        
        # Dual-Intent Architecture
        intent_res = predict_task("intent")
        intent_res.candidates = [{
            "model": intent_res.method,
            "label": intent_res.label,
            "confidence": intent_res.confidence
        }]
        if self.registry.has("minilm_intent"):
            minilm_res = predict_task("minilm_intent")
            
            intent_res.candidates.append({
                "model": minilm_res.method,
                "label": minilm_res.label,
                "confidence": minilm_res.confidence
            })
            
            if minilm_res.label != "unknown" and (intent_res.label == "unknown" or minilm_res.confidence > intent_res.confidence):
                candidates = intent_res.candidates
                intent_res = minilm_res
                intent_res.candidates = candidates

        # 9. ABSA (Aspect-Based Sentiment Analysis)
        absa_results = []
        
        # Build a mapping of tokens to their noun chunks for richer aspect names
        chunk_map = {}
        for chunk in doc.noun_chunks:
            for token in chunk:
                if token.pos_ in {"NOUN", "PROPN"}:
                    # Only map the core noun to the full chunk text
                    chunk_map[token.i] = chunk.text.lower()
                    
        for token in doc:
            aspect = None
            descriptor = None
            
            # Pattern 1: Noun + Adjective modifier (e.g. "torn box")
            if token.dep_ == "amod" and token.head.pos_ in {"NOUN", "PROPN"}:
                aspect = chunk_map.get(token.head.i, token.head.text.lower())
                descriptor = token.text.lower()
                
            # Pattern 2: Predicate Adjective (e.g. "box is torn")
            elif token.dep_ == "acomp" and token.head.pos_ in {"AUX", "VERB"}:
                subj = next((w for w in token.head.children if w.dep_ in {"nsubj", "nsubjpass"}), None)
                if subj and subj.pos_ in {"NOUN", "PROPN"}:
                    aspect = chunk_map.get(subj.i, subj.text.lower())
                    descriptor = token.text.lower()
                    
            if aspect and descriptor:
                # determine polarity
                desc_score = self.sia.polarity_scores(descriptor)["compound"]
                if desc_score >= 0.05: polarity = "Positive"
                elif desc_score <= -0.05: polarity = "Negative"
                else: polarity = "Neutral"
                
                # manual overrides for domain words
                if descriptor in {"torn", "broken", "broke", "error", "fail", "terrible", "crashed"}: polarity = "Negative"
                if descriptor in {"excellent", "great", "awesome", "perfect", "good"}: polarity = "Positive"
                
                if not any(a["aspect"] == aspect and a["descriptor"] == descriptor for a in absa_results):
                    absa_results.append({
                        "aspect": aspect,
                        "descriptor": descriptor,
                        "sentiment": polarity
                    })

        absa_res = [AspectResult(**a) for a in absa_results]

        # 10. CHURN RISK
        churn_keywords = {"cancel", "canceling", "cancelling", "refund", "quit", "leave", "unsubscribe", "close account"}
        churn_evidence = [t for t in text.lower().split() if any(k in t for k in churn_keywords)]
        if churn_evidence:
            churn_res = ChurnResult(label="high_risk", score=0.9, method="rules", evidence=churn_evidence)
        else:
            churn_res = ChurnResult(label="low_risk", score=0.1, method="rules", evidence=[])

        # 11. URGENCY
        urgency_evidence = []
        if "ERROR" in text: urgency_evidence.append("ERROR keyword")
        if "!" in text: urgency_evidence.append("exclamation marks")
        if churn_evidence: urgency_evidence.append("churn risk detected")
        if sent_label == "negative": urgency_evidence.append("negative sentiment")
        
        is_urgent = (sent_label == "negative" and (len(urgency_evidence) >= 2)) or ("ERROR" in text)
        urgency_res = UrgencyResult(
            label="High Priority" if is_urgent else "Low Priority",
            score=0.9 if is_urgent else 0.1,
            method="rules",
            evidence=urgency_evidence
        )

        # 12. UNIFIED AnalysisResult
        return AnalysisResponse(
            analysis_id=analysis_id,
            status="success",
            language=language_res,
            statistics=stats_res,
            linguistics=ling_res,
            sentiment=sent_res,
            spam=spam_res,
            intent=intent_res,
            absa=absa_res,
            urgency=urgency_res,
            churn=churn_res
        )
