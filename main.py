from docx import Document
from parser import iter_paragraphs
from run_mapper import RunMapper
from hybrid_detector import HybridDetector
from entity_filter import EntityFilter
from entity_normalizer import EntityNormalizer

def read_docx(file_path):

    doc = Document(file_path)
    detector = HybridDetector()
    filter = EntityFilter()
    normalizer = EntityNormalizer()

    for ref in iter_paragraphs(doc):

        if not ref.text.strip():
            continue

        mapper = RunMapper(ref)

        entities = detector.detect(mapper.text)
        entities = normalizer.normalize(entities)
        entities = filter.filter(entities)

        if not entities:
            continue

        print("=" * 80)
        print(mapper.text)

        for entity in entities:

            print(entity)

        # count += 1

        # if count == 10:
        #     break

read_docx('./input/Red_Herring_Prospectus.docx')
