import sys
import os
import json
from collections import defaultdict

sys.path.append(os.path.abspath("src"))
from mdas.application.analysis_service import AnalysisService

print("Loading Analysis Service...")
service = AnalysisService("models")

with open("tests/regression/classification_100.json", "r") as f:
    dataset = json.load(f)

intent_correct = 0
spam_correct = 0
intent_total = 0
spam_total = 0

intent_failures = []
spam_failures = []
confusion = defaultdict(lambda: defaultdict(int))

print("Evaluating 100 cases...")
for i, case in enumerate(dataset):
    text = case["text"]
    expected_intent = case["expected_intent"].lower()
    expected_spam = case["expected_spam"].lower()
    
    res = service.analyze(text, "test")
    
    if getattr(res, "status", None) == "unsupported_language":
        print(f"Skipping (Unsupported Language): {text}")
        continue
        
    # 1. Evaluate Spam
    actual_spam = res.spam.label.lower()
    if actual_spam == expected_spam:
        spam_correct += 1
    else:
        spam_failures.append({
            "text": text,
            "expected": expected_spam,
            "actual": actual_spam,
            "confidence": res.spam.confidence
        })
    spam_total += 1
    
    # 2. Evaluate Intent (if not spam and expected is not unknown)
    if expected_intent != "unknown":
        actual_intent = res.intent.label.lower()
        selected_model = res.intent.method
        confidence = res.intent.confidence
        
        legacy_pred = next((c for c in res.intent.candidates if (c.model if hasattr(c, "model") else c["model"]) == "legacy_model"), None)
        minilm_pred = next((c for c in res.intent.candidates if (c.model if hasattr(c, "model") else c["model"]) == "minilm_intent"), None)
        
        confusion[expected_intent][actual_intent] += 1
        
        if actual_intent == expected_intent:
            intent_correct += 1
        else:
            legacy_label = legacy_pred.label if hasattr(legacy_pred, "label") else legacy_pred["label"] if legacy_pred else "N/A"
            legacy_conf = legacy_pred.confidence if hasattr(legacy_pred, "confidence") else legacy_pred["confidence"] if legacy_pred else 0.0
            
            minilm_label = minilm_pred.label if hasattr(minilm_pred, "label") else minilm_pred["label"] if minilm_pred else "N/A"
            minilm_conf = minilm_pred.confidence if hasattr(minilm_pred, "confidence") else minilm_pred["confidence"] if minilm_pred else 0.0
            
            intent_failures.append({
                "text": text,
                "expected": expected_intent,
                "actual": actual_intent,
                "selected_model": selected_model,
                "confidence": confidence,
                "legacy_pred": f"{legacy_label} ({legacy_conf:.3f})" if legacy_pred else "N/A",
                "minilm_pred": f"{minilm_label} ({minilm_conf:.3f})" if minilm_pred else "N/A"
            })
        intent_total += 1

# Generate Markdown Report
report = [
    "# Classification Validation Report",
    "",
    "## 1. Executive Summary",
    f"- **Spam Accuracy**: {spam_correct}/{spam_total} ({(spam_correct/spam_total)*100:.1f}%)",
    f"- **Intent Accuracy**: {intent_correct}/{intent_total} ({(intent_correct/intent_total)*100:.1f}%)",
    "",
    "## 2. Intent Confusion Matrix",
    "| Expected | Predicted | Count |",
    "|----------|-----------|-------|"
]

for exp, preds in confusion.items():
    for pred, count in preds.items():
        report.append(f"| {exp} | {pred} | {count} |")

report.extend([
    "",
    "## 3. Intent Failures & RCA",
])

if not intent_failures:
    report.append("No intent failures detected.")
else:
    for fail in intent_failures:
        report.extend([
            f"### Failed: '{fail['text']}'",
            f"- **Expected**: `{fail['expected']}`",
            f"- **Actual**: `{fail['actual']}` (Confidence: {fail['confidence']:.3f})",
            f"- **Selected Model**: {fail['selected_model']}",
            f"- **Legacy Candidate**: {fail['legacy_pred']}",
            f"- **MiniLM Candidate**: {fail['minilm_pred']}",
            "> **RCA**: The models are likely struggling to distinguish this phrasing from the actual predicted class. The fallback logic selected the wrong model or both models failed.",
            ""
        ])

report.extend([
    "## 4. Spam Failures",
])
if not spam_failures:
    report.append("No spam failures detected.")
else:
    for fail in spam_failures:
        report.extend([
            f"- **Text**: '{fail['text']}'",
            f"  - Expected: {fail['expected']}, Actual: {fail['actual']} ({fail['confidence']:.3f})",
        ])

with open("classification_validation_report.md", "w") as f:
    f.write("\n".join(report))

print("Validation complete. Report generated at classification_validation_report.md")
