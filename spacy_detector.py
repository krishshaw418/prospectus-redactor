import spacy
from model import Entity

class SpacyDetector:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def detect(self, text):
        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:
            entities.append(
                Entity(
                    raw_type=ent.label_,
                    entity_type=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    score=1.0,
                    text=ent.text,
                    source="spacy"
                )
            )

        return entities