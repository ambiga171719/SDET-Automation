"""Base Page Object for API endpoints."""

from playwright.async_api import APIResponse
from config.config import BASE_URL, HEADERS, API_TIMEOUT
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object for API interactions."""

    def __init__(self, api_request_context):
        """Initialize with Playwright API request context."""

        self.api = api_request_context
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.timeout = API_TIMEOUT

    async def get(self, endpoint: str, **kwargs) -> APIResponse:
        """Make GET request to endpoint."""

        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET Request -> {url}")

        response = await self.api.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

        logger.info(f"GET Response <- {response.status}")

        return response

    async def post(self, endpoint: str, data: dict = None, **kwargs) -> APIResponse:
        """Make POST request to endpoint."""

        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST Request -> {url} | Payload: {data}")

        response = await self.api.post(
            url,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

        logger.info(f"POST Response <- {response.status}")

        return response

    async def put(self, endpoint: str, data: dict = None, **kwargs) -> APIResponse:
        """Make PUT request to endpoint."""

        url = f"{self.base_url}{endpoint}"

        logger.info(f"PUT Request -> {url} | Payload: {data}")

        response = await self.api.put(
            url,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

        logger.info(f"PUT Response <- {response.status}")

        return response

    async def patch(self, endpoint: str, data: dict = None, **kwargs) -> APIResponse:
        """Make PATCH request to endpoint."""

        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH Request -> {url} | Payload: {data}")

        response = await self.api.patch(
            url,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

        logger.info(f"PATCH Response <- {response.status}")

        return response

    async def delete(self, endpoint: str, **kwargs) -> APIResponse:
        """Make DELETE request to endpoint."""

        url = f"{self.base_url}{endpoint}"

        logger.info(f"DELETE Request -> {url}")

        response = await self.api.delete(
            url,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs
        )

        logger.info(f"DELETE Response <- {response.status}")

        return response

    async def get_json(self, response: APIResponse) -> dict:
        """Parse JSON from response."""
        return await response.json()