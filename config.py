from dataclasses import dataclass

@dataclass
class RouterConfig:
    light_model: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    heavy_model: str = "nlptown/bert-base-multilingual-uncased-sentiment"
    confidence_threshold: float = 0.85
    profanity_list: tuple = ('fuck', 'fucking', 'shit', 'damn', 'ass', 'hell', 'freaking', 'crap')
    log_file: str = "predictions.jsonl"