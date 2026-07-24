from presidio_detector import PresidioDetector
from spacy_detector import SpacyDetector


class HybridDetector:

    def __init__(self):
        self.presidio = PresidioDetector()
        self.spacy = SpacyDetector()

    def detect(self, text):
        entities = []

        entities.extend(self.presidio.detect(text))
        entities.extend(self.spacy.detect(text))

        return entities