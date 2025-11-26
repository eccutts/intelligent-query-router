# Sentiment Router

An intelligent query routing system that analyzes text sentiment and routes requests to appropriate ML models based on confidence and content signals.

## Architecture

- **Lightweight model**: DistilBERT (fast, lower accuracy)
- **Heavy model**: BERT multilingual (slower, higher accuracy)
- **Routing logic**: Escalates to heavy model when confidence < 85% or profanity detected

## Usage
```bash
pip install -r requirements.txt
python app.py
```

## Project Structure
```
├── app.py              # Entry point
├── config.py           # Configuration (thresholds, model names)
├── src/
│   ├── models.py       # Model loading and inference
│   ├── router.py       # Routing logic
│   └── logger.py       # Prediction logging
├── predictions.jsonl   # Logged predictions for analysis
└── requirements.txt
```

## Observations

- Base model (DistilBERT) was trained on movie reviews; fails on casual/slang language
- Profanity triggers false negatives regardless of actual sentiment
- Structured logging enables analysis of escalation patterns and model disagreements

## Next Steps

- [ ] Add entity extraction (spaCy)
- [ ] Integrate LLM for response generation
- [ ] Deploy to SageMaker
- [ ] Fine-tune on informal text data