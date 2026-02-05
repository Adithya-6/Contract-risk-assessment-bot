
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def classify_contract_type(text):
    text_lower = text.lower()
    if "employment" in text_lower:
        return "Employment Agreement"
    if "lease" in text_lower or "rent" in text_lower:
        return "Lease Agreement"
    if "partnership" in text_lower:
        return "Partnership Deed"
    if "vendor" in text_lower:
        return "Vendor Contract"
    return "Service Agreement"

def extract_clauses(text):
    clauses = re.split(r'\n|\.|;', text)
    return [c.strip() for c in clauses if len(c.strip()) > 40]

def process_contract(text):
    doc = nlp(text)
    clauses = extract_clauses(text)

    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)

    return {
        "clauses": clauses,
        "entities": entities
    }
