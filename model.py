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