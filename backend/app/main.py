from __future__ import annotations

import re
import traceback

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.bootstrap import bootstrap_admin
from app.database import Base, engine
from app.routers import auth, dashboard, logs, messages, numbers, users, webhook

app = FastAPI(title="Multi-Number SMS Manager", version="0.1.0")

_STARTUP_ERROR: str | None = None


def _redact_secrets(s: str) -> str:
    s = re.sub(r"(postgres(?:ql)?://[^:\s]+:)([^@\s]+)(@)", r"\1***\3", s)
    s = re.sub(r"(TWILIO_AUTH_TOKEN=)(\S+)", r"\1***", s)
    return s


@app.on_event("startup")
def _startup() -> None:
    global _STARTUP_ERROR
    try:
        Base.metadata.create_all(bind=engine)
        bootstrap_admin()
    except Exception:
        tb = _redact_secrets(traceback.format_exc())
        _STARTUP_ERROR = tb
        print("Startup failed:")
        print(tb)


app.include_router(auth.router)
app.include_router(numbers.router)
app.include_router(messages.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(logs.router)
app.include_router(webhook.router)


@app.get("/health")
def health() -> dict[str, str]:
    if _STARTUP_ERROR:
        return {"status": "error", "startup_error": _STARTUP_ERROR}
    return {"status": "ok"}
