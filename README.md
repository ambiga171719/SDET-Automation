# SDET REST API Test Suite – Playwright + Pytest + POM

A comprehensive REST API testing suite using **Playwright API mode**, **pytest**, and **Page Object Model (POM)** pattern. Tests the JSONPlaceholder API with full schema validation, parametrized tests, and performance benchmarks.

## Project Structure

```
sdet-playwright-submission/
├── tests/
│   ├── test_posts.py           # Tests for Posts endpoints
│   ├── test_users.py           # Tests for Users/nested resources
│   └── conftest.py             # Pytest configuration and fixtures
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base class for all API pages
│   ├── posts_page.py           # Posts API endpoints
│   └── users_page.py           # Users API endpoints
├── helpers/
│   ├── assertions.py           # Custom assertion helpers
│   └── schema_validator.py     # Pydantic models and JSON schemas
├── config/
│   └── config.py               # Configuration (BASE_URL, headers, timeout)
├── fixtures/
│   └── api_client.py           # Pytest fixtures (API context, page objects)
├── reports/                    # Test results and HTML reports
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # This file
└── .github/
    └── workflows/
        └── api-tests.yml       # GitHub Actions CI/CD pipeline
```

### Project Structure Notes
- **pages/** and **fixtures/** directories are intentional deviations from the minimal template
- **pages/**: Implements Page Object Model pattern for API testing
- **fixtures/**: Centralizes pytest fixtures for reusable test dependencies
- This enhanced structure improves maintainability, scalability, and separation of concerns

## Installation

### Prerequisites
- Python 3.10+ (required for union type syntax: `int | str`)
- pip

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd sdet-playwright-submission
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   python -m playwright install
   ```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test class:
```bash
pytest tests/test_posts.py::TestGetPosts
```

### Run specific test:
```bash
pytest tests/test_posts.py::TestGetPosts::test_get_all_posts_returns_200
```

### Run tests with specific markers:
```bash
pytest -m smoke          # Run smoke tests
pytest -m critical       # Run critical tests
pytest -m negative       # Run negative tests
pytest -m performance    # Run performance tests
pytest -m security       # Run security tests (injection, XSS, headers)
pytest -m "smoke or critical"  # Run both smoke and critical tests
```

### Run with verbose output:
```bash
pytest -v
```

### Run tests against custom API:
```bash
BASE_URL=https://your-api.com pytest
```

### Generate HTML report only:
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Coverage

### Posts Endpoints (`test_posts.py`)

**TestGetPosts:**
- ✅ GET /posts - fetch all posts, validate list
- ✅ GET /posts/{id} - fetch single post by ID (parametrized: 1, 10, 50, 100)
- ✅ GET /posts/{id} - invalid IDs (0, -1, 99999, "abc") → 404/400

**TestCreatePost:**
- ✅ POST /posts - create with valid payload → 201
- ✅ POST /posts - parametrized users (1, 5, 10)
- ✅ POST /posts - empty payload → 201/400
- ✅ POST /posts - missing required fields → 201/400
- ✅ POST /posts - empty title → 400 (negative)
- ✅ POST /posts - empty body → 400 (negative)
- ✅ POST /posts - invalid user ID type → 400 (negative)

**TestUpdatePost:**
- ✅ PUT /posts/{id} - full update → 200
- ✅ PUT /posts/{id} - multiple posts (1, 10, 50)
- ✅ PUT /posts/{id} - invalid ID → 400/404 (negative)
- ✅ PUT /posts/{id} - empty title → 400 (negative)
- ✅ PUT /posts/{id} - empty body → 400 (negative)
- ✅ PATCH /posts/{id} - partial update → 200
- ✅ PATCH /posts/{id} - non-existent post

**TestDeletePost:**
- ✅ DELETE /posts/{id} - delete post → 200/204
- ✅ DELETE /posts/{id} - specific 204 status test
- ✅ DELETE /posts/{id} - multiple posts
- ✅ DELETE /posts/{id} - non-existent post

**TestChainedRequests:**
- ✅ Create → Retrieve → Delete workflow
- ✅ Create → Update → Retrieve → Delete workflow

**TestPerformance:**
- ✅ Response time validation for GET /posts
- ✅ Response time validation for GET /posts/{id}

**TestResponseHeaders:**
- ✅ Content-Type validation for GET, POST, PUT, PATCH, DELETE
- ✅ Header presence validation across all HTTP methods
- ✅ Assertion helper: `assert_header_present()`

### Users Endpoints (`test_users.py`)

**TestUserPosts:**
- ✅ GET /users/{id}/posts - fetch user posts → 200
- ✅ GET /users/{id}/posts - parametrized users (1, 2, 5, 10)
- ✅ GET /users/{id}/posts - invalid user → 200/404
- ✅ Verify all posts belong to requested user

**TestUserPostsNegative:**
- ✅ Special characters in user ID
- ✅ Float user ID
- ✅ Boundary values (-9999, 0, 1, 9999)

**TestGetUserById:**
- ✅ GET /users/{id} - fetch user by ID → 200
- ✅ GET /users/{id} - schema validation with UserSchema
- ✅ GET /users/{id} - parametrized users (1, 5, 10)
- ✅ GET /users/{id} - invalid user ID → 404/400 (negative)
- ✅ GET /users/{id} - invalid ID formats (0, -1, "abc") → 404/400
- ✅ GET /users/{id} - required fields validation

## Architecture & Design Patterns

### Page Object Model (POM)
- **BasePage** (`pages/base_page.py`): Base class with HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **PostsPage** (`pages/posts_page.py`): Page object for Posts API endpoints
- **UsersPage** (`pages/users_page.py`): Page object for Users API endpoints
- **Benefit**: Centralized API interactions, easy maintenance, reduced code duplication

### Fixtures (Dependency Injection)
- `api_context`: Playwright APIRequestContext
- `posts_api`: PostsPage instance
- `users_api`: UsersPage instance
- `post_payload`: Sample post data
- `invalid_payloads`: Invalid test data for negative tests

-### Test Organization
- **Markers**: `smoke`, `critical`, `negative`, `performance`, `security`
- **Parametrization**: Multiple test cases from single test function
- **Async/Await**: Native async support with pytest-asyncio

### Schema Validation
- **Pydantic Models**: `PostResponseSchema`, `UserSchema`
- **JSON Schema**: `POST_RESPONSE_SCHEMA`, `POSTS_LIST_SCHEMA`, `USER_POSTS_SCHEMA`
- **Custom Assertions**: `validate_schema()`, `assert_status_code()`, etc.

## Configuration

Edit `config/config.py` to customize:
```python
BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
HEADERS = {"Content-Type": "application/json"}
API_TIMEOUT = 10000  # milliseconds
```

## Test Statistics

- **Total Test Cases**: 82
- **Smoke Tests**: 8
- **Critical Tests**: 15
- **Security Tests**: 4
- **Negative Tests**: 18
- **Performance Tests**: 2
- **Response Header Tests**: 6
- **Parametrized Test Combinations**: 20+
- **Schema Validation Tests**: Full coverage with Pydantic + JSON Schema

## AI Tools Used

1. **GitHub Copilot**: Generated initial test structure, POM base classes, and assertion helpers, accelerating development by providing intelligent code suggestions based on context.
2. **Copilot Chat**: Assisted with debugging async/await patterns in Playwright API mode and validating schema validation approaches.


## Assumptions About System Under Test

1. **API Availability**: JSONPlaceholder is publicly accessible at https://jsonplaceholder.typicode.com
2. **Response Format**: All endpoints return valid JSON with Content-Type: application/json
3. **Status Codes**: 
   - POST creates return 201
   - Successful operations return 200
   - Invalid requests may return 400 or 404
   - Deletions may return 200 or 204
4. **Idempotency**: Mock API accepts and acknowledges all requests (doesn't validate as strictly as production APIs)
5. **No Authentication**: API is public, no auth headers required

## Bonus Challenges Implemented

- ✅ **Schema Validation**: Pydantic models + JSON Schema validation for responses
- ✅ **Response Time Assertions**: Performance test class with timing validation
- ✅ **Parametrized Tests**: Multiple input combinations using `@pytest.mark.parametrize`
- ✅ **Nested Resources**: Tests for GET /users/{id}/posts endpoint
- ✅ **Chained Requests**: Multi-step workflows (create → retrieve → delete)
- ✅ **CI/CD Integration**: GitHub Actions workflow with matrix testing (3.10, 3.11, 3.12)
- ✅ **Page Object Model**: Complete POM implementation for API interactions
- ✅ **Negative Testing**: Comprehensive negative test class for each endpoint
- ✅ **Test Markers**: Organized with smoke, critical, negative, performance and security markers
- ✅ **Async Testing**: Full async/await support with pytest-asyncio

## Running Specific Test Scenarios

### All CRUD operations:
```bash
pytest tests/test_posts.py -v
```

### Only happy path tests:
```bash
pytest -m "smoke or critical" -v
```

### Only error scenarios:
```bash
pytest -m negative -v
```

### Single workflow test:
```bash
pytest tests/test_posts.py::TestChainedRequests::test_create_retrieve_delete_post_workflow -v
```

## Troubleshooting

**Import errors:**
```bash
# Ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**Async timeout issues:**
- Increase `API_TIMEOUT` in `config/config.py`
- Add `asyncio_mode = auto` to `pytest.ini` (already configured)

**Network issues:**
- Verify internet connectivity
- Check BASE_URL configuration
- Use VPN if API is geographically restricted

## Contributing

When adding new tests:
1. Follow POM pattern—add methods to appropriate Page Object
2. Use fixtures from `fixtures/api_client.py`
3. Add test markers (smoke, critical, negative, performance, security)
4. Write descriptive docstrings
5. Use parameterization for multiple similar test cases


