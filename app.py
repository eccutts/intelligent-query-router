import gradio as gr
from config import RouterConfig
from src.router import SentimentRouter

print("Loading models...")
config = RouterConfig()
router = SentimentRouter(config)
print("Ready!")

def analyze(text):
    if not text.strip():
        return "Enter some text to analyze"
    return router.route(text)

demo = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(label="Enter text", placeholder="I love mashed potatoes..."),
    outputs=gr.Textbox(label="Analysis", lines=5),
    title="Sentiment Router",
    description="Analyses sentiment, extracts entities, and generates a response. Uses dual-model routing with confidence-based escalation."
)

demo.launch(share=True)