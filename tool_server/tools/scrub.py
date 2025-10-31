from fastapi import APIRouter
from pydantic import BaseModel
import re, spacy

router = APIRouter()
nlp = spacy.load("de_core_news_sm")

class TextIn(BaseModel):
    text: str

@router.post("/scrub")
def scrub_text(item: TextIn):
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<EMAIL_REDACTED>", item.text)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("PER","ORG","LOC"):
            text = text.replace(ent.text, f"<{ent.label_}_REDACTED>")
    return {"clean_text": text}

tool_spec = {
    "name": "scrub",
    "description": "Entfernt PII (E-Mail, Namen, Orte) aus Texten.",
    "parameters": {"text": {"type": "string", "description": "zu bereinigender Text"}},
    "endpoint": "/scrub",
    "method": "POST",
    "output_key": "clean_text",
}
