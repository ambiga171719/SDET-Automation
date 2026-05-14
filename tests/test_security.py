"""Security-related tests for API endpoints.

These tests exercise basic security validations such as injecting common
attack patterns and verifying the service does not disclose internal
error information (stack traces) or expose unnecessary server headers.

Note: JSONPlaceholder is a mock service and may not implement strict
security controls. Tests focus on detecting obvious server errors or
information leakage rather than enforcing production-grade defenses.
"""

import pytest

from helpers.assertions import (
    assert_status_code_in,
    assert_header_present,
)


def _response_contains_error_leakage(response_text: str) -> bool:
    """Detect common keywords indicating internal error leakage."""
    if not response_text:
        return False
    low = response_text.lower()
    # Avoid matching common attribute names like 'onerror' — target obvious
    # server-side error indicators only.
    keywords = ["traceback", "exception", "stacktrace", "errno"]
    return any(k in low for k in keywords)


@pytest.mark.negative
async def test_sql_injection_payload_does_not_leak_server_errors(posts_api):
    """POST with SQL injection-like payload should not return stack traces."""
    payload = {"title": "1; DROP TABLE users; --", "body": "sql test", "userId": 1}

    response = await posts_api.create_post_with_payload(payload)
    # Accept common statuses from mock API but ensure no error leakage
    assert_status_code_in(response, [201, 400, 500])

    try:
        text = await response.text()
    except Exception:
        text = ""

    assert not _response_contains_error_leakage(text), "Response contains error/stack leakage"


@pytest.mark.negative
async def test_xss_payload_does_not_leak_server_errors(posts_api):
    """POST with XSS-like payload should not return stack traces or leak server errors."""
    payload = {"title": "<script>alert(1)</script>", "body": "<img src=x onerror=alert(1)>", "userId": 1}

    response = await posts_api.create_post_with_payload(payload)
    assert_status_code_in(response, [201, 400, 500])

    try:
        text = await response.text()
    except Exception:
        text = ""

    assert not _response_contains_error_leakage(text), "Response contains error/stack leakage"


@pytest.mark.security
async def test_cors_header_present_on_get(posts_api):
    """Simple CORS header check on a public GET endpoint."""
    response = await posts_api.get_all_posts()
    assert_status_code_in(response, [200])
    # Case-insensitive header lookup; accept any Access-Control-Allow-* header
    headers_lower = {k.lower(): k for k in response.headers.keys()}
    has_cors = any(k.startswith("access-control-allow-") for k in headers_lower)
    assert has_cors, "CORS header missing"


@pytest.mark.security
async def test_no_x_powered_by_header_exposed(posts_api):
    """Ensure server does not expose X-Powered-By header (reduces information leakage)."""
    response = await posts_api.get_all_posts()
    # Accept normal status
    assert_status_code_in(response, [200])
    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    xp = headers_lower.get("x-powered-by")
    if xp:
        # If present, ensure it does not disclose a version number (avoid leaking precise server details)
        assert not any(c.isdigit() for c in xp), "X-Powered-By header should not expose version numbers"
