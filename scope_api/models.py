from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Session(BaseModel):
    """Minimal representation of a scoping session as produced by the CLI/web.

    `answers` is intentionally flexible to allow evolution of the question set
    without breaking older sessions.
    """

    id: str
    version: str = "0.1.0"
    answers: Dict[str, Any]


class EnrichedSession(Session):
    summary: Optional[str] = None
    questions_for_client: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
  
