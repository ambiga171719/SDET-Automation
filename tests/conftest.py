# conftest.py - Pytest configuration and fixtures for API tests
"""Pytest configuration."""
import pytest, logging, sys
from pathlib import Path

# Add project root to Python import path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import fixtures so pytest can discover them
from fixtures.api_client import api_context, posts_api, users_api, post_payload, invalid_payloads

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)