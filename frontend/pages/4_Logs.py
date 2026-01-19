from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from lib.api_client import api_get
from lib.auth import require_login, sidebar

st.set_page_config(page_title="Audit Logs - SMS Manager", page_icon="📜", layout="wide")

require_login()
sidebar()

st.title("📜 Audit Logs")
st.caption("A record of all actions taken within the system.")

try:
    logs = api_get("/logs", params={"limit": 500})
    if not logs:
        st.info("No log entries found.")
    else:
        df = pd.DataFrame(logs)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        if "action" in df.columns:
            action_map = {
                "twilio_inbound_sms": "Inbound SMS",
                "forward_message": "Forwarded SMS",
                "login": "Login",
                "update_number": "Update Number",
                "create_user": "Create User",
                "update_user": "Update User",
            }
            def _friendly_action(s: str) -> str:
                v = str(s or "").strip()
                key = v.lower()
                if key in action_map:
                    return action_map[key]
                return re.sub(r"\btwilio\b\s*", "", v, flags=re.IGNORECASE).strip() or v

            df["action"] = df["action"].astype(str).apply(_friendly_action)
        st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Failed to load audit logs: {e}")
