from docx import Document
from parser import iter_paragraphs
from run_mapper import RunMapper
from hybrid_detector import HybridDetector
from entity_filter import EntityFilter
from entity_normalizer import EntityNormalizer
from run_redactor import RunRedactor

def read_docx(file_path):

    doc = Document(file_path)
    detector = HybridDetector()
    filter = EntityFilter()
    normalizer = EntityNormalizer()
    redactor = RunRedactor()

    for ref in iter_paragraphs(doc):

        if not ref.text.strip():
            continue

        mapper = RunMapper(ref)

        entities = detector.detect(mapper.text)
        entities = normalizer.normalize(entities)
        entities = filter.filter(entities)

        if not entities:
            continue

        redactor.redact(mapper, entities)

        output_path = "./output/redacted.docx"

        doc.save(output_path)

    print(f"Redaction complete! Saved redacted document at {output_path}")

read_docx('./input/Red_Herring_Prospectus.docx')
