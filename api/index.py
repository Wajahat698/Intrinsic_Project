import os
import sys

# Ensure the backend package imports work when running in Vercel's serverless environment.
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app  # noqa: E402
