from src.models import SentimentModels
from src.logger import PredictionLogger
from src.entities import EntityExtractor
from src.responder import Responder
from config import RouterConfig

class SentimentRouter:
    """
    Core routing logic: analyze sentiment, extract entities, escalate if uncertain, generate response.
    """
    
    def __init__(self, config: RouterConfig):
        self.config = config
        self.models = SentimentModels(config.light_model, config.heavy_model)
        self.logger = PredictionLogger(config.log_file)
        self.entity_extractor = EntityExtractor()
        self.responder = Responder()
    
    def _has_profanity(self, text: str) -> bool:
        words = text.lower().split()
        return any(word in self.config.profanity_list for word in words)
    
    def _needs_escalation(self, score: float, text: str) -> tuple[bool, str]:
        # Profanity triggers escalation because light model learned profanity = negative
        if self._has_profanity(text):
            return True, "profanity"
        # Low confidence = model is uncertain, get second opinion
        if score < self.config.confidence_threshold:
            return True, "low_confidence"
        return False, None
    
    def route(self, text: str) -> str:
        light_result = self.models.predict_light(text)
        escalate, reason = self._needs_escalation(light_result["score"], text)
        entities = self.entity_extractor.extract(text)
        
        log_entry = {
            "input": text,
            "entities": entities,
            "light_model": light_result,
            "escalated": escalate,
            "reason": reason,
            "heavy_model": None
        }
        
        if escalate:
            heavy_result = self.models.predict_heavy(text)
            log_entry["heavy_model"] = heavy_result
            sentiment_str = f"{heavy_result['label']}"
        else:
            sentiment_str = f"{light_result['label']}"
        
        topic = entities["noun_chunks"][0] if entities["noun_chunks"] else "unknown"
        
        response = self.responder.generate(text, sentiment_str, topic)
        log_entry["response"] = response
        self.logger.log(log_entry)
        
        return f"{sentiment_str} | topic: {topic}\n→ {response}"