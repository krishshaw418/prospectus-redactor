from model import Entity
import re


class EntityFilter:

    PRIORITY = {
        "EMAIL_ADDRESS": 100,
        "PHONE_NUMBER": 90,
        "CREDIT_CARD": 80,
        "SSN": 80,
        "IP_ADDRESS": 70,
        "COMPANY": 65,
        "PERSON": 60,
    }

    BLACKLIST = {
        "Offer",
        "Promoter",
        "Promoters",
        "Director",
        "Directors",
        "Company",
        "Board",
        "Shareholder",
        "Shareholders",
        "Reference Rate",
        "Fiscals",
        "Pursuant",
        "Excludes",
        "Alpha",
        "Beta",
    }

    LOCATION_KEYWORDS = (
        "Village",
        "Taluka",
        "District",
        "Road",
        "Street",
        "Facility",
        "Industrial Park",
    )

    ISO_PATTERN = re.compile(r"^ISO\s+\d+")

    def filter(self, entities: list[Entity]) -> list[Entity]:

        entities = self._remove_overlapping(entities)
        entities = self._remove_false_positives(entities)

        return entities

    def _remove_overlapping(self, entities):

        entities = sorted(
            entities,
            key=lambda e: (
                e.start,
                -(e.end - e.start),
                -self.PRIORITY.get(e.entity_type, 0),
            ),
        )

        filtered = []

        for entity in entities:

            keep = True

            for existing in filtered:

                overlap = (
                    entity.start < existing.end
                    and entity.end > existing.start
                )

                if overlap:

                    if (
                        self.PRIORITY.get(entity.entity_type, 0)
                        <= self.PRIORITY.get(existing.entity_type, 0)
                    ):
                        keep = False
                        break

            if keep:
                filtered.append(entity)

        return filtered

    def _remove_false_positives(self, entities):

        filtered = []

        for entity in entities:

            if not self._is_valid(entity):
                continue

            filtered.append(entity)

        return filtered

    def _is_valid(self, entity):

        text = entity.text.strip()

        if text in self.BLACKLIST:
            return False

        if self.ISO_PATTERN.fullmatch(text):
            return False

        if any(keyword in text for keyword in self.LOCATION_KEYWORDS):
            return False

        if (
            entity.entity_type == "COMPANY"
            and len(text.split()) < 2
        ):
            return False

        if (
            entity.entity_type == "PERSON"
            and len(text.split()) < 2
        ):
            return False

        if re.fullmatch(r"\d{4}", text):
            return False

        return True