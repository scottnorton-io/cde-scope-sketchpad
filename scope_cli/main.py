"""CLI entrypoint for Local CDE Scope Sketchpad.

Prompts the user through a small, opinionated set of CDE scoping questions
and writes two artifacts per run:

- sessions/<id>-session.json
- sessions/<id>-sketch.md

This module is intentionally dependency-light so it can run both inside
Docker and directly on the host.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import typer
import yaml

app = typer.Typer(help="Local CDE Scope Sketchpad CLI")

BASE_DIR = Path(__file__).resolve().parents[1]
SESSIONS_DIR = BASE_DIR / "sessions"
QUESTIONS_PATH = BASE_DIR / "scope_cli" / "questions.yaml"


def load_questions() -> Dict[str, Any]:
    with QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _prompt(q: Dict[str, Any]) -> Any:
    """Prompt for a single answer based on question metadata.

    v1 keeps parsing simple; answers are stored mostly as strings, with
    light handling for multi_choice.
    """

    prompt = q["prompt"]
    q_type = q.get("type", "string")

    if q_type == "multi_choice":
        raw = typer.prompt(f"{prompt} ")
        return [part.strip() for part in raw.split(",") if part.strip()]

    if q_type in {"choice", "string"}:
        return typer.prompt(f"{prompt} ")

    # Fallback for text / unknown types
    return typer.prompt(f"{prompt} ")


def _render_markdown_sketch(session: Dict[str, Any]) -> str:
    answers: Dict[str, Any] = session.get("answers", {})

    engagement_name = answers.get("engagement_name") or "Unnamed engagement"
    channels = answers.get("channels") or []
    channels_str = ", ".join(channels) if isinstance(channels, list) else str(channels)
    stores_pan = answers.get("stores_pan_anywhere", "unsure")
    segmentation_present = answers.get("segmentation_present", "unsure")

    return f"""# CDE Scope Sketch – {engagement_name}

Session ID: {session["id"]}
Version: {session.get("version", "0.1.0")}

## High-level notes

- Payment channels: {channels_str}
- Stores PAN anywhere: {stores_pan}
- Segmentation present: {segmentation_present}

## CDE flow (Mermaid skeleton)
```mermaid
flowchart LR
  Client[Cardholder]
  App[Application]
  Proc[Processor]
  Store[(Data Store)]

  Client --> App
  App --> Proc
  App --> Store
```

## Free-form notes

Add additional scoping details here as the engagement evolves.

"""

@app.command()
def sketch() -> None:
    """Run a scoping session and write JSON + Markdown artifacts."""

    questions = load_questions()
    version = questions.get("version", "0.1.0")
    session: Dict[str, Any] = {
        "id":
        "id": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "version": version,
        "answers": {},
    }

    for section in questions.get("sections", []):
        typer.echo("")
        typer.echo(f"== {section.get('title', section.get('id', 'Section'))} ==")
        for q in section.get("questions", []):
            answer = _prompt(q)
            session["answers"][q["id"]] = answer
            SESSIONS_DIR.mkdir(exist_ok=True, parents=True)
            safe_id = session["id"].replace(":", "-")
            json_path = SESSIONS_DIR / f"{safe_id}-session.json"
            md_path = SESSIONS_DIR / f"{safe_id}-sketch.md"
            json_path.write_text(json.dumps(session, indent=2), encoding="utf-8")
            md_path.write_text(_render_markdown_sketch(session), encoding="utf-8")
            typer.echo("")
            typer.echo(f"Saved session JSON:  {json_path}")
            typer.echo(f"Saved sketch markdown: {md_path}")
            if name == "**main**":  # pragma: no cover
                app()
