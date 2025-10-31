# ---- Basis-Image (schlank, mit Python 3.12) ----
FROM python:3.12-slim

# ---- Umgebungsvariablen ----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- Systemabhängigkeiten (für spaCy, word-docx etc.) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Arbeitsverzeichnis ----
WORKDIR /app

# ---- Requirements kopieren & installieren ----
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- spaCy deutsches Modell installieren ----
RUN python -m spacy download de_core_news_sm

# ---- App-Dateien kopieren ----
COPY . .

# ---- Exponierter Port ----
EXPOSE 8000

# ---- Startbefehl ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
