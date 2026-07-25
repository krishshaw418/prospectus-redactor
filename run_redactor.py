from run_mapper import RunMapper


class RunRedactor:

    REPLACEMENTS = {
        "PERSON": "[PERSON]",
        "COMPANY": "[COMPANY]",
        "EMAIL_ADDRESS": "[EMAIL]",
        "PHONE_NUMBER": "[PHONE]",
        "SSN": "[SSN]",
        "IP_ADDRESS": "[IP]",
        "DATE_OF_BIRTH": "[DOB]",
        "CREDIT_CARD": "[CARD]",
    }

    def redact(self, mapper: RunMapper, entities):
        """
        Redact all entities in a paragraph while preserving formatting.
        """

        if not entities:
            return

        entities = sorted(
            entities,
            key=lambda e: e.start,
            reverse=True
        )

        for entity in entities:
            self._redact_entity(mapper, entity)

    def _replacement(self, entity):
        return self.REPLACEMENTS.get(
            entity.entity_type,
            "[REDACTED]"
        )

    def _redact_entity(self, mapper, entity):

        matches = mapper.find_runs(entity.start, entity.end)

        if not matches:
            return

        replacement = self._replacement(entity)

        if len(matches) == 1:

            match = matches[0]

            text = match.run.text

            before = text[:match.local_start]
            after = text[match.local_end:]

            match.run.text = before + replacement + after

            return
        
        first = matches[0]

        first_before = first.run.text[:first.local_start]

        first.run.text = first_before + replacement

        for middle in matches[1:-1]:
            middle.run.text = ""

        last = matches[-1]

        last_after = last.run.text[last.local_end:]

        last.run.text = last_after