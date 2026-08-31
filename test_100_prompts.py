import urllib.request
import json
import time
import random

prompts = [
    "I received the Adidas shoes today at my Mumbai office. The tracking updates were excellent, but the packaging box was completely torn!",
    "ERROR! The new desktop update completely broke my profile sync feature on Windows 11. Fix this broken loop immediately or I am canceling my monthly subscription!",
    "Can you add a custom dark mode theme to the dashboard menu? I am looking at buying the enterprise package next week but I want to check if the price is fixed.",
    "The package was damaged by the courier.",
    "The courier damaged the package, but the replacement was delivered by the warehouse.",
    "I want a refund right now. This is terrible.",
    "How do I reset my password?",
    "Where is my order? It was supposed to arrive yesterday.",
    "Thank you for the quick support, the issue is resolved.",
    "I hate this new update, it crashes every time I open the app.",
]

# Generate more variations to reach 100
subjects = ["laptop", "phone", "software", "service", "app", "delivery", "payment", "subscription"]
adjectives = ["great", "terrible", "broken", "fast", "slow", "expensive", "cheap", "amazing"]
verbs = ["bought", "canceled", "upgraded", "downgraded", "returned", "received"]
for i in range(90):
    text = f"I {random.choice(verbs)} the {random.choice(subjects)}. It is {random.choice(adjectives)}. "
    if random.random() > 0.5:
        text += "Please fix it immediately!"
    else:
        text += "Thank you."
    prompts.append(text)

results = []
start_time = time.time()
errors = 0

for i, p in enumerate(prompts):
    req = urllib.request.Request(
        'http://127.0.0.1:8006/api/v1/analyze', 
        data=json.dumps({'text': p}).encode(), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        t0 = time.time()
        with urllib.request.urlopen(req) as f:
            res = json.loads(f.read().decode())
            results.append({
                "latency": time.time() - t0,
                "intent": res["intent"]["label"],
                "spam": res["spam"]["label"],
                "voice": res["linguistics"]["voice"]["summary_label"]
            })
    except Exception as e:
        errors += 1

total_time = time.time() - start_time
print(f"Total Requests: 100")
print(f"Success: {len(results)}, Errors: {errors}")
print(f"Total Time: {total_time:.2f}s")
if results:
    avg_lat = sum(r["latency"] for r in results) / len(results)
    print(f"Average Latency: {avg_lat*1000:.2f}ms")
    intents = {}
    voices = {}
    for r in results:
        intents[r["intent"]] = intents.get(r["intent"], 0) + 1
        voices[r["voice"]] = voices.get(r["voice"], 0) + 1
    print(f"Intents Distribution: {intents}")
    print(f"Voice Distribution: {voices}")
