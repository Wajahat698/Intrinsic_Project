from __future__ import annotations

import os

import httpx
import streamlit as st

_API_BASE_URL_CACHE: str | None = None


def get_api_base_url() -> str:
    global _API_BASE_URL_CACHE
    if _API_BASE_URL_CACHE:
        return _API_BASE_URL_CACHE

    secrets_api_base_url = None
    try:
        secrets_api_base_url = st.secrets.get("API_BASE_URL")
    except Exception:
        secrets_api_base_url = None

    _API_BASE_URL_CACHE = (
        secrets_api_base_url
        or os.getenv("API_BASE_URL")
        or "http://127.0.0.1:8000"
    ).strip().rstrip("/")
    return _API_BASE_URL_CACHE

def _auth_headers() -> dict[str, str]:
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

def api_post(path: str, json_data: dict):
    base_url = get_api_base_url()
    from lib.embedded_backend import ensure_backend_started
    ensure_backend_started(base_url)
    with httpx.Client(timeout=20) as client:
        r = client.post(f"{base_url}{path}", json=json_data, headers=_auth_headers())
        r.raise_for_status()
        return r.json()

def api_get(path: str, params: dict | None = None):
    base_url = get_api_base_url()
    from lib.embedded_backend import ensure_backend_started
    ensure_backend_started(base_url)
    with httpx.Client(timeout=20) as client:
        r = client.get(f"{base_url}{path}", headers=_auth_headers(), params=params)
        r.raise_for_status()
        return r.json()

def api_patch(path: str, json_data: dict):
    base_url = get_api_base_url()
    from lib.embedded_backend import ensure_backend_started
    ensure_backend_started(base_url)
    with httpx.Client(timeout=20) as client:
        r = client.patch(f"{base_url}{path}", headers=_auth_headers(), json=json_data)
        r.raise_for_status()
        return r.json()

def api_put(path: str, json_data: dict):
    base_url = get_api_base_url()
    from lib.embedded_backend import ensure_backend_started
    ensure_backend_started(base_url)
    with httpx.Client(timeout=20) as client:
        r = client.put(f"{base_url}{path}", headers=_auth_headers(), json=json_data)
        r.raise_for_status()
        return r.json()
