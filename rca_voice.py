from mdas.nlp.spacy_backend import SpacyBackend
from mdas.analysis.linguistics import analyze_linguistics
from mdas.analysis.voice import analyze_voice
from mdas.application.analysis_service import AnalysisService

import json

sb = SpacyBackend()
srv = AnalysisService("models")

texts = [
    "The company released the update.",
    "The update was released by the company.",
    "The company released the update. The update was released by the company."
]

print("==================== VOICE RCA ====================")
for text in texts:
    print(f"\n--- Text: {text} ---")
    doc = sb.process(text)
    
    # 3. Raw result returned by voice analyzer
    voice_raw = analyze_voice(doc)
    print("3. Raw Voice Result:", json.dumps(voice_raw, indent=2))
    
    # 4. Value received by AnalysisService
    # Simulation of AnalysisService logic
    ling_raw = analyze_linguistics(doc, include_token_details=False)
    v_raw = ling_raw.get("voice", {})
    
    # 5. Pydantic API Serialized Value
    res = srv.analyze(text, "rca-123")
    print("\n5. Serialized Voice API Result:")
    print(json.dumps(res.linguistics.voice.dict(), indent=2))
    
print("\nSpam and Intent tests on legacy:")
res2 = srv.analyze("I received the Adidas shoes today at my Mumbai office. The tracking updates were excellent, but the packaging box was completely torn!", "rca-124")
print("Adidas Spam:", res2.spam.dict())
print("Adidas Intent:", res2.intent.dict())

res3 = srv.analyze("ERROR! The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!", "rca-125")
print("Error Spam:", res3.spam.dict())
print("Error Intent:", res3.intent.dict())
