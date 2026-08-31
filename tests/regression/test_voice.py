import sys
import os

sys.path.append(os.path.abspath("src"))

from mdas.application.analysis_service import AnalysisService

print("Loading Analysis Service...")
service = AnalysisService("models")

VOICE_TESTS = [
    ("The team fixed the problem.", "active"),
    ("The problem was fixed by the team.", "passive"),
    ("The problem was fixed.", "passive"),
    ("The team is fixing the problem.", "active"),
    ("The problem is being fixed.", "passive"),
    ("The system crashed.", "active"),
    ("The system is stable.", "linking"),
    ("The package is damaged.", "linking"),
    ("The package was damaged by the courier.", "passive"),
    ("The update was released yesterday.", "passive"),
    ("The update is available.", "linking"),
    ("We received the package and it was damaged.", "mixed"),
    ("The company released the update, which was later criticized.", "mixed")
]

correct = 0
failed = []

print("\nRunning Voice Regression Tests...")
print("-" * 40)
for text, expected in VOICE_TESTS:
    res = service.analyze(text, "test")
    actual = res.linguistics.voice.summary_label.lower()
    
    if actual == expected.lower():
        correct += 1
    else:
        failed.append(f"FAIL: '{text}' | Expected: {expected} | Actual: {actual}")

print(f"\nVOICE")
print("-" * 24)
print(f"{len(VOICE_TESTS)} tests")
print(f"{correct} correct")
print(f"{len(failed)} incorrect\n")
if failed:
    for f in failed:
        print(f)
        
accuracy = (correct / len(VOICE_TESTS)) * 100
print(f"\nAccuracy: {accuracy:.1f}%\n")
