from transformers import pipeline

class SentimentModels:
    def __init__(self, light_model: str, heavy_model: str):
        print("Loading lightweight model...")
        self.light = pipeline("sentiment-analysis", model=light_model)
        
        print("Loading heavy model...")
        self.heavy = pipeline("sentiment-analysis", model=heavy_model)
        
        print("Models ready.")
    
    def predict_light(self, text: str) -> dict:
        result = self.light(text)[0]
        return {"label": result["label"], "score": result["score"]}
    
    def predict_heavy(self, text: str) -> dict:
        result = self.heavy(text)[0]
        return {"label": result["label"], "score": result["score"]}