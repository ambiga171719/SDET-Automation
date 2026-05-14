import pytest

from helpers.assertions import (
    assert_status_code_in,
    assert_header_present,
)


class TestSecurity:

    @staticmethod
    def _response_contains_error_leakage(response_text: str) -> bool:
        """Detect common keywords indicating internal error leakage."""
        if not response_text:
            return False
        low = response_text.lower()
        keywords = ["traceback", "exception", "stacktrace", "errno"]
        return any(k in low for k in keywords)

    @pytest.mark.negative
    async def test_sql_injection_payload_does_not_leak_server_errors(self, posts_api):
        payload = {"title": "1; DROP TABLE users; --", "body": "sql test", "userId": 1}

        response = await posts_api.create_post_with_payload(payload)
        assert_status_code_in(response, [201, 400, 500])

        try:
            text = await response.text()
        except Exception:
            text = ""

        assert not self._response_contains_error_leakage(text)

    @pytest.mark.negative
    async def test_xss_payload_does_not_leak_server_errors(self, posts_api):
        payload = {
            "title": "<script>alert(1)</script>",
            "body": "<img src=x onerror=alert(1)>",
            "userId": 1
        }

        response = await posts_api.create_post_with_payload(payload)
        assert_status_code_in(response, [201, 400, 500])

        try:
            text = await response.text()
        except Exception:
            text = ""

        assert not self._response_contains_error_leakage(text)

    @pytest.mark.security
    async def test_cors_header_present_on_get(self, posts_api):
        response = await posts_api.get_all_posts()
        assert_status_code_in(response, [200])

        headers_lower = {k.lower(): k for k in response.headers.keys()}
        has_cors = any(k.startswith("access-control-allow-") for k in headers_lower)
        assert has_cors

    @pytest.mark.security
    async def test_no_x_powered_by_header_exposed(self, posts_api):
        response = await posts_api.get_all_posts()
        assert_status_code_in(response, [200])

        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        xp = headers_lower.get("x-powered-by")

        if xp:
            assert not any(c.isdigit() for c in xp)