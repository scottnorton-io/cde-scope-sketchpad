# scope_api/app.py

from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .llm_client import LLMClient
from .models import EnrichedSession, Session


app = FastAPI(title="CDE Scope Sketchpad API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if exposed beyond localhost
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = LLMClient()
BASE_DIR = Path(__file__).resolve().parents[1]
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True, parents=True)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/enrich", response_model=EnrichedSession)
async def enrich(session: Session) -> EnrichedSession:
    """Enrich a scoping session with optional AI-generated notes.

    Behavior:
    - Always returns a valid EnrichedSession.
    - If the local LLM is unavailable, falls back to deterministic notes only.
    """

    enriched = EnrichedSession(**session.dict())
    enriched.notes.append("Enrichment run completed (v0.1).")

    prompt_lines: List[str] = [
        "You are a PCI DSS assessor helping to clarify CDE scope.",
        "Summarize the scope in 2–3 sentences, then list 3–5 clarifying questions.",
        "Here is a JSON object with scoping answers:",
        session.json(indent=2),
    ]
    prompt = "\n\n".join(prompt_lines)

    summary = await llm_client.summarize(prompt)
    if summary:
        enriched.summary = summary

    out_path = SESSIONS_DIR / f"{session.id}-enriched.json"
    try:
        out_path.write_text(enriched.json(indent=2), encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))

    return enriched
