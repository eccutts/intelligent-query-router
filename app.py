from config import RouterConfig
from src.router import SentimentRouter

def main():
    config = RouterConfig()
    router = SentimentRouter(config)
    
    print("\nSentiment Router ready.\n")
    
    while True:
        text = input("Enter text (or 'quit'): ")
        if text.lower() == 'quit':
            break
        print(router.route(text))

if __name__ == "__main__":
    main()