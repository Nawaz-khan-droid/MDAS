import sys
from pathlib import Path
sys.path.insert(0, "src")
from mdas.analyzer import MDASAnalyzer

def test_sarcasm():
    analyzer = MDASAnalyzer.from_directory("models")
    
    prompts = [
        "Oh wonderful, another update that breaks all my workflows. Great job guys.",
        "Fantastic, my screen is completely frozen again.",
        "What a brilliant idea to remove the save button. Now I've lost everything.",
        "Your customer service is stellar, I've been on hold for three hours.",
        "I just wanted to say that your new update is fantastic. It saved me hours of work!"
    ]
    
    print("\n--- SARCASM EVALUATION ---")
    for p in prompts:
        print(f"\nPrompt: {p}")
        res = analyzer.analyze(p)
        print(f"Sentiment: {res.classification['sentiment']['label']}")
        print(f"Sarcasm Score: {res.signals['sarcasm']['score']} ({res.signals['sarcasm']['label']})")
        print(f"Category: {res.classification['category']['label']}")
        print(f"Intent: {res.classification['intent']['label']}")

if __name__ == '__main__':
    test_sarcasm()
