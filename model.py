from enum import Enum

class Location(Enum):
    BODY = "body"
    TABLE = "table"
    HEADER = "header"
    FOOTER = "footer"


class ParagraphRef:

    def __init__(self, paragraph, location: Location):
        self.paragraph = paragraph
        self.location = location
        self.runs = paragraph.runs
        self.text = "".join(run.text for run in self.runs)

    def __str__(self):
        return f"[{self.location.name}] {self.text}"

    def __repr__(self):
        return self.__str__()

class Entity:

    def __init__(
        self,
        raw_type,
        entity_type,
        start,
        end,
        score,
        text,
        source,
    ):   
        self.raw_type = raw_type
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.score = score
        self.text = text
        self.source = source

    def __repr__(self):
        return (
            f"Entity("
            f"type={self.entity_type}, "
            f"start={self.start}, "
            f"end={self.end}, "
            f"score={self.score:.2f}, "
            f"text={repr(self.text)})"
        )