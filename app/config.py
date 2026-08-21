"""Application configuration loaded from environment variables.

Uses python-dotenv so a local .env file is picked up during development.
In production, real environment variables take precedence.
"""

import os

from dotenv import load_dotenv

# Load variables from a .env file if present (no-op if the file is missing).
load_dotenv()

APP_ENV: str = os.getenv("APP_ENV", "development")
PORT: int = int(os.getenv("PORT", "8000"))