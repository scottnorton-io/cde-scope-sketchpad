from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


API_BASE_URL = "http://scope-api:8000"  # overridden via env in Docker if needed

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
SESSIONS_DIR = BASE_DIR.parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True, parents=True)

app = FastAPI(title="CDE Scope Sketchpad – Web UI")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(TEMPLATES_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/session", response_class=HTMLResponse)
async def create_session(
    request: Request,
    engagement_name: str = Form(""),
    assessor_initials: str = Form(""),
    channels: str = Form(""),
    stores_pan_anywhere: str = Form("unsure"),
    tokenization: str = Form(""),
    pan_transit_summary: str = Form(""),
    providers: str = Form(""),
    segmentation_present: str = Form("unsure"),
    segmentation_notes: str = Form(""),
    open_questions_list: str = Form(""),
) -> HTMLResponse:
    answers: Dict[str, Any] = {
        "engagement_name": engagement_name,
        "assessor_initials": assessor_initials,
        "channels": [c.strip() for c in channels.split(",") if c.strip()],
        "stores_pan_anywhere": stores_pan_anywhere,
        "tokenization": tokenization,
        "pan_transit_summary": pan_transit_summary,
        "providers": providers,
        "segmentation_present": segmentation_present,
        "segmentation_notes": segmentation_notes,
        "open_questions_list": open_questions_list,
    }

    payload: Dict[str, Any] = {
        "id": "web-session",  # scope-api will still enrich consistently
        "version": "0.1.0",
        "answers": answers,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{API_BASE_URL}/enrich", json=payload)
    resp.raise_for_status()
    enriched = resp.json()

    mermaid = _render_mermaid(enriched)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "session": enriched,
            "mermaid_diagram": mermaid,
        },
    )


def _render_mermaid(session: Dict[str, Any]) -> str:
    answers = session.get("answers", {})
    channels = answers.get("channels") or []
    if isinstance(channels, list):
        channel_label = ", ".join(channels)
    else:
        channel_label = str(channels)

    return f"""
```mermaid
flowchart LR
  Client[Cardholder]
  App[Application]
  Proc[Processor]
  Store[(Data Store)]

  Client --> App
  App --> Proc
  App --> Store

  %% Channels: {channel_label}
```
"""
