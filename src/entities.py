import spacy

class EntityExtractor:
    """
    Extracts what the sentence is about using spaCy NLP.
    Identifies named entities (people, orgs, places) and noun chunks (topics).
    """
    
    def __init__(self):
        # Small model trades accuracy for speed; upgrade to en_core_web_lg for production
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract(self, text: str) -> dict:
        doc = self.nlp(text)
        
        # Named entities: proper nouns (Amazon=ORG, Seattle=GPE, Erik=PERSON)
        named_entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Grammatical subjects/objects
        subjects = [token.text for token in doc if token.dep_ in ("nsubj", "dobj", "pobj")]
        
        # Noun chunks: multi-word concepts like "mashed potatoes"
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() != "i"]
        
        return {
            "named_entities": named_entities,
            "subjects": subjects,
            "noun_chunks": noun_chunks
        }