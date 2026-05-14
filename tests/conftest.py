# conftest.py - Pytest configuration and fixtures for API tests
"""Pytest configuration."""
import pytest, logging, sys

from datetime import datetime
from pathlib import Path


# Import fixtures so pytest can discover them
from fixtures.api_client import api_context, posts_api, users_api, post_payload, invalid_payloads

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    config.option.htmlpath = f"reports/{timestamp}/report.html"
    config.option.xmlpath = f"reports/{timestamp}/junit.xml"