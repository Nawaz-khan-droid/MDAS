from mdas.application.analysis_service import AnalysisService
import json
import uuid

service = AnalysisService("models")

cases = [
    "I received the Adidas shoes today at my Mumbai office. The tracking updates were excellent, but the packaging box was completely torn!",
    "The problem was fixed by our support team.",
    "ERROR! The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!"
]

for i, text in enumerate(cases, 1):
    print(f"\n==================== TEST CASE {i} ====================")
    print(f"TEXT: {text}")
    res = service.analyze(text, str(uuid.uuid4()))
    
    print("\n[ NER ]")
    for e in res.linguistics.entities:
        print(f"  {e.text} -> {e.label}")
        
    print("\n[ VOICE ]")
    print(f"Overall: {res.linguistics.voice.summary_label}")
    for s in res.linguistics.voice.sentences: # Note: field is sentences in schema
        print(f"  [{s.label}] {s.text}  | Evidence: {s.evidence}")
        
    print("\n[ ABSA ]")
    for a in res.absa:
        print(f"  {a.aspect} -> {a.descriptor} ({a.sentiment})")
        
    print("\n[ STATISTICS ]")
    print(f"  Words: {res.statistics.words} | Tokens: {res.statistics.tokens} | Sentences: {res.statistics.sentences} | Paragraphs: {res.statistics.paragraphs} | Time: {res.statistics.reading_time}")

    print("\n[ INTENT ]")
    print(f"  {res.intent.label} ({res.intent.confidence}) | Model: {res.intent.method}")

    print("\n[ SPAM ]")
    print(f"  {res.spam.label} ({res.spam.confidence})")
