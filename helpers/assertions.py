
from jsonschema import validate, ValidationError

# Custom assertion helper functions for API tests
def assert_status_code(response, expected_code):
    """Assert response status code matches expected code."""
    actual_code = response.status
    assert actual_code == expected_code, (
        f"Expected status code {expected_code}, got {actual_code}"
    )


def assert_status_code_in(response, expected_codes):
    """Assert response status code is in list of expected codes."""
    actual_code = response.status
    assert actual_code in expected_codes, (
        f"Expected status code in {expected_codes}, got {actual_code}"
    )


def assert_content_type(response):
    """Assert response contains JSON content-type."""
    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, (
        f"Expected JSON content-type, got {content_type}"
    )

def assert_content_type_json(response):
    """Assert response has JSON content-type (strict check)."""
    content_type = response.headers.get("content-type", "")
    assert content_type.startswith("application/json"), (
        f"Expected application/json content-type, got {content_type}"
    )

def assert_header_present(response, header_name):
    """Assert specific header exists in response."""
    headers = response.headers
    header_names_lower = {k.lower(): k for k in headers.keys()}
    assert header_name.lower() in header_names_lower, (
        f"Expected header '{header_name}' not found. Available headers: {list(headers.keys())}"
    )


def assert_response_field(data, field_name):
    """Assert response data contains specific field."""
    assert field_name in data, (
        f"Expected field '{field_name}' not found in response. Keys: {list(data.keys())}"
    )


def assert_field_value(data, field_name, expected_value):
    """Assert response field has expected value."""
    actual_value = data.get(field_name)
    assert actual_value == expected_value, (
        f"Expected field '{field_name}' to be {expected_value}, got {actual_value}"
    )


def validate_schema(data, schema):
    """Validate data against JSON schema."""
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")

def assert_list_not_empty(data):
    """Assert response is non-empty list."""

    assert isinstance(data, list), (
        f"Expected list, got {type(data)}"
    )

    assert len(data) > 0, "Expected non-empty list"

def assert_is_list(data):
    """Assert response data is a list."""

    assert isinstance(data, list), (
        f"Expected list, got {type(data)}"
    )


def assert_response_time(elapsed_ms, max_ms):
    """Assert response time is under specified milliseconds."""
    
    assert elapsed_ms < max_ms, (
        f"Response took {elapsed_ms:.2f}ms, expected under {max_ms}ms"
    )
