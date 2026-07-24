from docx.text.run import Run
from model import ParagraphRef

class RunInfo:

    def __init__(self, run, start, end):
        self.run = run
        self.start = start
        self.end = end

    @property
    def text(self):
        return self.run.text

    def __repr__(self):
        return(
            f"RunInfo(start={self.start}, "
            f"end={self.end}, "
            f"text={repr(self.text)})"
        )

class RunMapper:

    def __init__(self, paragraph_ref: ParagraphRef):

        self.paragraph_ref = paragraph_ref

        self.text = ""
        self.run_infos = []

        self._build_mapping()

    def _build_mapping(self):

        current_position = 0

        for run in self.paragraph_ref.runs:

            start = current_position

            self.text += run.text

            current_position += len(run.text)

            end = current_position

            self.run_infos.append(
                RunInfo(run, start, end)
            )

    def find_runs(self, start: int, end: int):

        matches = []

        for run_info in self.run_infos:

            if run_info.end <= start:
                continue

            if run_info.start >= end:
                continue

            local_start = max(start, run_info.start) - run_info.start
            local_end = min(end, run_info.end) - run_info.start

            matches.append(
                RunMatch(
                    run_info,
                    local_start,
                    local_end
                )
            )

        return matches

class RunMatch:

    def __init__(
        self,
        run_info: RunInfo,
        local_start: int,
        local_end: int
    ):
        self.run_info = run_info
        self.local_start = local_start
        self.local_end = local_end

    @property
    def run(self):
        return self.run_info.run

    @property
    def text(self):
        return self.run.text

    @property
    def matched_text(self):
        return self.text[self.local_start:self.local_end]

    def __repr__(self):
        return (
            f"RunMatch("
            f"global=({self.run_info.start}, {self.run_info.end}), "
            f"local=({self.local_start}, {self.local_end}), "
            f"matched={repr(self.matched_text)}, "
            f"text={repr(self.text)})"
        )