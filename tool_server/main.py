import copy
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tools.scrub import router as scrub_router, tool_spec as scrub_spec

app = FastAPI(title="Local Tool Server", version="1.0")

# --- CORS (wichtig für OpenWebUI) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oder ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrub_router)

BASE_URL = os.getenv("TOOL_SERVER_BASE_URL", "http://localhost:8000")


# --- Tool-Spezifikation für OpenWebUI ---
@app.get("/toolspec")
def get_toolspec():
    spec = copy.deepcopy(scrub_spec)
    if not spec["endpoint"].startswith("http"):
        spec["endpoint"] = f"{BASE_URL}{spec['endpoint']}"
    spec.setdefault("base_url", BASE_URL)
    return {"tools": [spec]}


@app.get("/")
def root():
    return {"status": "Tool Server running", "toolspec": "/toolspec", "base_url": BASE_URL}
