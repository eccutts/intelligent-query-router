from huggingface_hub import InferenceClient
import re

class Responder:
    """
    Generates contextual responses using a hosted LLM.
    Uses free Hugging Face Inference API — swap model for quality/cost tradeoffs.
    """
    
    def __init__(self):
        self.client = InferenceClient()
    
    def _clean(self, text: str) -> str:
        # Remove common instruction-tuned model artifacts
        text = re.sub(r'\[/?ASS.*?\]', '', text)
        text = re.sub(r'\[/?USER.*?\]', '', text)
        text = re.sub(r'\[/?INST.*?\]', '', text)
        return text.strip().split('\n')[0]
    
    def generate(self, text: str, sentiment: str, topic: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a friendly assistant. Respond in ONE short sentence only. Never exceed 15 words."
            },
            {
                "role": "user",
                "content": f"Someone said: \"{text}\"\nTheir sentiment about {topic} is {sentiment}. Acknowledge this briefly."
            }
        ]

        response = self.client.chat_completion(
            messages=messages,
            model="HuggingFaceH4/zephyr-7b-beta",
            max_tokens=50
        )
        return self._clean(response.choices[0].message.content)