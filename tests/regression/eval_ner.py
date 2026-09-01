import sys
import os

sys.path.append(os.path.abspath("src"))

from mdas.application.analysis_service import AnalysisService

print("Loading Analysis Service...")
service = AnalysisService("models")

NER_TESTS = [
    ("Adidas released a new shoe today in Mumbai.", {"Adidas": "ORG", "today": "DATE", "Mumbai": "LOCATION"}),
    ("Microsoft and Google compete globally.", {"Microsoft": "ORG", "Google": "ORG"}),
    ("The monthly update for Apple is here.", {"Apple": "ORG"}), # 'monthly' should be ignored
    ("It was built by John Doe in London.", {"John Doe": "PERSON", "London": "LOCATION"}),
]

correct = 0
failed = []

print("\nRunning NER Regression Tests...")
print("-" * 40)
for text, expected in NER_TESTS:
    res = service.analyze(text, "test")
    actual = {e.text: e.label for e in res.linguistics.entities}
    
    if actual == expected:
        correct += 1
    else:
        failed.append(f"FAIL: '{text}'\n  Expected: {expected}\n  Actual:   {actual}")

print(f"\nNER")
print("-" * 24)
print(f"{len(NER_TESTS)} tests")
print(f"{correct} correct")
print(f"{len(failed)} incorrect\n")
if failed:
    for f in failed:
        print(f)
        
accuracy = (correct / len(NER_TESTS)) * 100
print(f"\nAccuracy: {accuracy:.1f}%\n")
