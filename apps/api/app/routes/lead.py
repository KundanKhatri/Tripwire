"""POST /lead — capture a security-review lead from the Test-Your-Agent flow.

No database on the prototype: leads are emitted as structured logs, so they're
durably queryable in Azure Container Apps log analytics. Swap in a table / CRM
webhook later without changing the client contract.
"""

from __future__ import annotations

import json
import logging
import re

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["lead"])

_log = logging.getLogger("tripwire.lead")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class LeadRequest(BaseModel):
    email: str = Field(..., max_length=200)
    agent_context: str = Field("", max_length=2000)
    message: str = Field("", max_length=2000)
    grade: str = Field("", max_length=4)
    source: str = Field("test-your-agent", max_length=60)


class LeadResponse(BaseModel):
    ok: bool
    error: str | None = None


@router.post("/lead", response_model=LeadResponse)
async def capture_lead(req: LeadRequest) -> LeadResponse:
    if not _EMAIL_RE.match(req.email.strip()):
        return LeadResponse(ok=False, error="Please enter a valid email address.")

    # Structured, queryable, and PII-minimal in the log line.
    _log.info(
        "LEAD %s",
        json.dumps(
            {
                "email": req.email.strip(),
                "grade": req.grade,
                "source": req.source,
                "agent_context": req.agent_context[:500],
                "message": req.message[:500],
            }
        ),
    )
    return LeadResponse(ok=True)
