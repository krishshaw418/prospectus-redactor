from docx import Document
from parser import iter_paragraphs
from run_mapper import RunMapper

def read_docx(file_path):

    doc = Document(file_path)

    for ref in iter_paragraphs(doc):

        if not ref.text.strip():
            continue

        mapper = RunMapper(ref)

        print("=" * 80)
        print(mapper.text)

        for run_info in mapper.run_infos:
            print(run_info)

        print("\nMatched Runs:")
        matches = mapper.find_runs(18, 25)

        for match in matches:
            print(match)

        break
read_docx('./input/Red_Herring_Prospectus.docx')
