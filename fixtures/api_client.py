"""API Fixtures for tests."""
import pytest
from playwright.async_api import async_playwright
from pages.posts_page import PostsPage
from pages.users_page import UsersPage

@pytest.fixture
async def api_context():
    """Create API context for each test.
    
    Yields:
        APIRequestContext
    """
    async with async_playwright() as p:
        context = await p.request.new_context()
        yield context
        await context.dispose()

# Fixture for Posts API page object
@pytest.fixture
async def posts_api(api_context):
    """Fixture to provide Posts API page object.
    
    Args:
        api_context: API request context
        
    Yields:
        PostsPage instance
    """
    yield PostsPage(api_context)

# Fixture for Users API page object - can be used in user-related tests
@pytest.fixture
async def users_api(api_context):
    """Fixture to provide Users API page object.
    
    Args:
        api_context: API request context
        
    Yields:
        UsersPage instance
    """
    yield UsersPage(api_context)

# Fixture for valid post payload - can be used in create/update tests
@pytest.fixture
def post_payload():
    """Fixture providing sample post payload.
    
    Returns:
        dict: Sample post data
    """
    return {
        "title": "Test Post Title",
        "body": "This is test post body content",
        "userId": 1
    }

# Fixture for invalid payloads - can be used in negative test cases
@pytest.fixture
def invalid_payloads():
    """Fixture providing invalid post payloads.
    
    Returns:
        list: List of invalid payloads
    """
    return [
        {},  # Empty payload
        {"title": "No body"},  # Missing body
        {"body": "No title"},  # Missing title
        {"title": "", "body": "", "userId": 1},  # Empty strings
    ]
