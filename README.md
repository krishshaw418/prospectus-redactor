# Prospectus Redaction Tool

A Python-based DOCX redaction tool that detects and redacts Personally Identifiable Information (PII) while preserving the original document's formatting, layout, tables, and styling.

## Approach

The redaction pipeline consists of the following stages:

```
DOCX
  │
  ▼
Parser
  │
  ▼
Run Mapper
  │
  ▼
Hybrid Entity Detection
  │
  ▼
Entity Normalization
  │
  ▼
Entity Filtering
  │
  ▼
Run Redaction
  │
  ▼
Redacted DOCX
```

### 1. Document Parsing
- Traverses all paragraphs, tables, nested tables, and table cells.
- Represents each paragraph using a `ParagraphRef` abstraction.

### 2. Run Mapping
- Builds a mapping between paragraph character offsets and Word runs.
- Enables redaction across multiple runs while preserving formatting.

### 3. Hybrid Entity Detection
Uses a combination of:
- **Microsoft Presidio** for PII detection (emails, phone numbers, SSNs, IPs, etc.)
- **spaCy** Named Entity Recognition for people and organizations
- **Regex-based detection** for pattern-based entities such as:
  - SSNs
  - Credit Card Numbers
  - IP Addresses
  - Dates of Birth (context-based)

### 4. Entity Normalization
Normalizes detector outputs into a common set of entity types used by the application.

### 5. Entity Filtering
Filters duplicate, overlapping, and low-confidence detections to reduce false positives.

### 6. Run Redaction
Replaces detected entities with placeholders (e.g. `[PERSON]`, `[EMAIL]`) without modifying the document structure or formatting.

---

## Supported Entity Types

| Entity | Status |
|---------|--------|
| Person Names | ✅ |
| Company Names | ✅ |
| Email Addresses | ✅ |
| Phone Numbers | ✅ |
| Social Security Numbers (SSNs) | ✅ |
| Credit Card Numbers | ✅ |
| IP Addresses | ✅ |
| Dates of Birth | ✅ (context-based) |
| Physical/Mailing Addresses | ⚠️ Partial |

---

## Current Limitations

- Physical/Mailing address detection is only partially supported. Free-form address extraction is significantly more complex and may require a dedicated address parser or a specialized NER model.
- Detection quality depends on the underlying NER models and may occasionally produce false positives or miss certain entities.

---

## Output

The generated document:
- Preserves fonts, styling, tables, and layout.
- Redacts detected PII using placeholder tokens.
- Produces a readable, structurally identical redacted DOCX.