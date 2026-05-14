# conftest.py - Pytest configuration and fixtures for API tests
"""Pytest configuration."""

import pytest
import logging
import sys
import time

from datetime import datetime
from pathlib import Path

# Import fixtures so pytest can discover them
from fixtures.api_client import api_context, posts_api, users_api, post_payload, invalid_payloads


# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ----------------------------
# Report Configuration
# ----------------------------
def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    config.option.htmlpath = f"reports/{timestamp}/report.html"
    config.option.xmlpath = f"reports/{timestamp}/junit.xml"


# ----------------------------
# Performance Tracking
# ----------------------------
performance_start_time = {}
performance_total_time = 0


def pytest_runtest_setup(item):
    if "performance" in item.keywords:
        performance_start_time[item.nodeid] = time.perf_counter()


def pytest_runtest_teardown(item):
    global performance_total_time

    if "performance" in item.keywords:
        start = performance_start_time.get(item.nodeid)

        if start is not None:   # ✅ safe check
            elapsed = (time.perf_counter() - start) * 1000
            performance_total_time += elapsed

            print(f"\n⏱ Performance: {item.name} → {elapsed:.2f} ms")


def pytest_sessionfinish(session, exitstatus):
    print("\n" + "=" * 60)
    print(f"🚀 Total Performance Test Execution Time: {performance_total_time:.2f} ms")
    print("=" * 60)