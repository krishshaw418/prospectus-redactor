from presidio_analyzer import AnalyzerEngine

from model import Entity

class PresidioDetector:

    def __init__(self):
        self.analyzer = AnalyzerEngine()

    def detect(self, text: str) -> list[Entity]:

        results = self.analyzer.analyze(
            text=text,
            language="en",
        )

        entities = []

        for result in results:

            entities.append(
                Entity(
                    raw_type=result.entity_type,
                    entity_type=result.entity_type,
                    start=result.start,
                    end=result.end,
                    score=result.score,
                    text=text[result.start:result.end],
                    source="presidio"
                )
            )

        return entities