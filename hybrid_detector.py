from presidio_detector import PresidioDetector
from spacy_detector import SpacyDetector
from regex_detector import RegexDetector


class HybridDetector:

    def __init__(self):
        self.presidio = PresidioDetector()
        self.spacy = SpacyDetector()
        self.regex = RegexDetector()

    def detect(self, text):
        entities = []

        entities.extend(self.presidio.detect(text))
        entities.extend(self.spacy.detect(text))
        entities.extend(self.regex.detect(text))

        return entities