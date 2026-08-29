from mdas import MDASAnalyzer

analyzer = MDASAnalyzer.from_directory("models")
result = analyzer.analyze(
    "Oh great, another outage. Truly stellar engineering work. "
    "Fix this immediately or cancel our subscription."
)
print(result.to_dict())
