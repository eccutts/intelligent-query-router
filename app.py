from transformers import pipeline
import json
from datetime import datetime

print("Loading lightweight model...")
light_model = pipeline("sentiment-analysis")

print("Loading powerful model...")
heavy_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

print("Ready!\n")

profanity_words = {'fuck', 'fucking', 'shit', 'damn', 'ass', 'hell', 'freaking', 'crap'}

def has_profanity(text):
    return any(word in text.lower().split() for word in profanity_words)

def route_request(text):
    result = light_model(text)[0]
    light_label = result['label']
    light_score = result['score']
    
    needs_escalation = light_score < 0.85 or has_profanity(text)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": text,
        "light_model": {"label": light_label, "score": light_score},
        "escalated": needs_escalation,
        "reason": None,
        "heavy_model": None
    }
    
    if needs_escalation:
        log_entry["reason"] = "profanity" if has_profanity(text) else "low_confidence"
        heavy_result = heavy_model(text)[0]
        log_entry["heavy_model"] = {"label": heavy_result['label'], "score": heavy_result['score']}
    
    with open("predictions.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    if needs_escalation:
        return f"ESCALATED ({log_entry['reason']}): {log_entry['heavy_model']['label']} ({log_entry['heavy_model']['score']:.2f})"
    else:
        return f"LIGHT MODEL: {light_label} ({light_score:.2f})"

while True:
    text = input("Enter text (or 'quit'): ")
    if text.lower() == 'quit':
        break
    print(route_request(text))