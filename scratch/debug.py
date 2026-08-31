import sys
sys.path.insert(0, "src")
from mdas.analyzer import MDASAnalyzer
analyzer = MDASAnalyzer.from_directory("models")
res = analyzer.analyze("Oh wonderful, another update that breaks all my workflows. Great job guys.")
print(res.classification.get("sarcasm"))
print(res.signals.get("sarcasm"))
