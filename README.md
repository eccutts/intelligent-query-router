# Intelligent Query Router

A sentiment-aware query routing system that analyzes text, extracts entities, and generates contextual responses using multiple ML models.

## Architecture

- **Lightweight model**: DistilBERT (fast, binary sentiment)
- **Heavy model**: BERT multilingual (slower, 1-5 star ratings)
- **Entity extraction**: spaCy NLP pipeline
- **Response generation**: Mistral-7B via Hugging Face Inference API
- **Routing logic**: Escalates to heavy model when confidence < 85% or profanity detected

## Usage
```bash
pip install -r requirements.txt
huggingface-cli login
python app.py
```

## Project Structure
```
├── app.py              # Entry point
├── config.py           # Configuration (thresholds, model names)
├── src/
│   ├── models.py       # Sentiment model loading and inference
│   ├── router.py       # Routing logic and orchestration
│   ├── entities.py     # spaCy entity extraction
│   ├── responder.py    # LLM response generation
│   └── logger.py       # Structured JSONL logging
├── predictions.jsonl   # Logged predictions for analysis
└── requirements.txt
```

## Key Observations

- DistilBERT (trained on movie reviews) misclassifies casual language and profanity
- Profanity triggers false negatives regardless of actual sentiment
- Escalation to heavier model improves accuracy on ambiguous inputs
- Free-tier LLMs produce usable but inconsistent response quality

## Next Steps

- [ ] Deploy to SageMaker
- [ ] Add aspect-based sentiment (per-entity scoring)
- [ ] Fine-tune on informal/slang text data
- [ ] Swap response LLM for higher quality (GPT-4, Claude)
```

Save. Now update **requirements.txt**:
```
transformers>=4.30.0
torch>=2.0.0
spacy>=3.5.0
huggingface_hub>=0.20.0