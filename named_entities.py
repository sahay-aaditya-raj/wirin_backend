from locationtagger import NamedEntityExtractor
import spacy

def name_extractor(text: str):
    e = NamedEntityExtractor(url=None, text=text)
    e.find_named_entities()
    return ' '.join(e.named_entities)


# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

def destination_from_text(text: str) -> str:
    doc = nlp(text.lower())
    
    # Define keywords related to destination requests
    destination_keywords = [
        "location", "where", "here", "there", "near", "far",
        "distance", "map", "gps", "address", "place", "navigate",
        "direction", "move", "go", "arrive", "travel", "route",
        "find", "explore", "to"
    ]

    destination = None

    # Iterate over the tokens in the text
    for token in doc:
        # Check if the token lemma (in lowercase) is a destination keyword
        if token.lemma_.lower() in destination_keywords:
            # Traverse the subtree of the token to find related nouns or proper nouns
            entity = name_extractor(text)
            if entity:
                return entity
                

    return destination