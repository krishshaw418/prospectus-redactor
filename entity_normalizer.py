class EntityNormalizer:

    TYPE_MAP = {
        "PERSON": "PERSON",
        "EMAIL_ADDRESS": "EMAIL_ADDRESS",
        "PHONE_NUMBER": "PHONE_NUMBER",
        "IP_ADDRESS": "IP_ADDRESS",
        "US_SSN": "SSN",
        "CREDIT_CARD": "CREDIT_CARD",
        "DATE_OF_BIRTH": "DATE_OF_BIRTH",
    }

    COMPANY_SUFFIXES = (
        "Private Limited",
        "Limited",
        "Ltd",
        "Ltd.",
        "LLP",
        "Inc",
        "Inc.",
        "Corporation",
        "Corp.",
        "Trust",
        "Foundation",
        "Bank Limited",
        "Bank",
    )

    def normalize(self, entities):
        normalized = []

        for entity in entities:
            entity = self._normalize(entity)

            if entity is not None:
                normalized.append(entity)

        return normalized

    def _normalize(self, entity):

        if entity.raw_type in self.TYPE_MAP:
            entity.entity_type = self.TYPE_MAP[entity.raw_type]
            return entity

        if self._looks_like_company(entity.text):
            entity.entity_type = "COMPANY"
            return entity

        return None

    def _looks_like_company(self, text: str) -> bool:
        text = text.strip()

        return (
            len(text.split()) > 1
            and text.endswith(self.COMPANY_SUFFIXES)
        )