import re
from model import Entity


class RegexDetector:

    SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    CREDIT_CARD = re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    )

    IPV4 = re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    )

    DOB = re.compile(
        r"(?i)(?:date of birth|dob|birth date)\s*[:\-]?\s*"
        r"([A-Za-z]+\s+\d{1,2},\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    )

    def detect(self, text):

        entities = []

        entities.extend(self._find(self.SSN, text, "SSN"))
        entities.extend(self._find(self.IPV4, text, "IP_ADDRESS"))
        entities.extend(self._find(self.CREDIT_CARD, text, "CREDIT_CARD"))

        for m in self.DOB.finditer(text):

            entities.append(
                Entity(
                    raw_type="DATE_OF_BIRTH",
                    entity_type="DATE_OF_BIRTH",
                    start=m.start(1),
                    end=m.end(1),
                    score=1.0,
                    text=m.group(1),
                    source="regex",
                )
            )

        return entities

    def _find(self, pattern, text, entity_type):

        entities = []

        for m in pattern.finditer(text):

            entities.append(
                Entity(
                    raw_type=entity_type,
                    entity_type=entity_type,
                    start=m.start(),
                    end=m.end(),
                    score=1.0,
                    text=m.group(),
                    source="regex",
                )
            )

        return entities