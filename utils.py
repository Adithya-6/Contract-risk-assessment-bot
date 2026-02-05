
import fitz
import docx
from langdetect import detect

def extract_text_from_file(file_path, file_type):
    if "pdf" in file_type:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif "docx" in file_type:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def detect_language(text):
    try:
        return "Hindi" if detect(text) == "hi" else "English"
    except:
        return "English"

def normalize_text(text):
    return text.replace("\n", " ").strip()
