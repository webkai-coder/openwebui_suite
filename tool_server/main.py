from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Local Tool Server", version="1.0")

# --- CORS (wichtig für OpenWebUI) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Input/Output Schemas ---
class TextIn(BaseModel):
    text: str

class TextOut(BaseModel):
    clean_text: str

# --- Haupttool ---
@app.post("/scrub", response_model=TextOut, summary="Scrub Text")
def scrub_text(data: TextIn):
    cleaned = data.text.replace("Kai", "[REDACTED_NAME]")
    return {"clean_text": cleaned}

# --- Tool-Spezifikation für OpenWebUI ---
@app.get("/toolspec")
def get_toolspec():
    return {
        "tools": [
            {
                "name": "scrub",
                "description": "Entfernt persönliche Daten aus Texten.",
                "parameters": {
                    "text": {"type": "string", "description": "Zu bereinigender Text"}
                },
                "endpoint": "/scrub",
                "method": "POST",
                "output_key": "clean_text",
            }
        ]
    }
@app.get("/")
def root():
    return {"status": "Tool Server running", "toolspec": "/toolspec"}
