from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


def _ensure_sqlite_dir(url: str) -> None:
    if not url.startswith("sqlite"):
        return
    if not url.startswith("sqlite:///"):
        return

    sqlite_path = url[len("sqlite:///") :]
    if not sqlite_path:
        return

    p = Path(sqlite_path)
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()

    parent = p.parent
    parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_dir(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
