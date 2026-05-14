"""Tests for Users API endpoints."""
import pytest
from helpers.assertions import (
    assert_status_code,
    assert_status_code_in,
    assert_content_type,
    assert_response_field,
    assert_list_not_empty,
    validate_schema,
    assert_header_present
)
from helpers.schema_validator import USER_POSTS_SCHEMA, UserSchema


class TestUserPosts:
    """Test GET /users/{id}/posts endpoint."""

    @pytest.mark.smoke
    @pytest.mark.critical
    async def test_get_user_posts_returns_200(self, users_api):
        """Test getting posts for valid user returns 200."""
        user_id = 1
        response = await users_api.get_user_posts(user_id)
        assert_status_code(response, 200)
        assert_content_type(response)
        
        data = await users_api.get_json(response)
        assert_list_not_empty(data)
        validate_schema(data, USER_POSTS_SCHEMA)

    @pytest.mark.parametrize("user_id", [1, 2, 5, 10])
    async def test_get_user_posts_multiple_users(self, users_api, user_id):
        """Test getting posts for multiple valid users."""
        response = await users_api.get_user_posts(user_id)
        assert_status_code(response, 200)
        
        data = await users_api.get_json(response)
        if isinstance(data, list) and len(data) > 0:
            # Verify all posts belong to the requested user
            for post in data:
                assert post.get("userId") == user_id

    @pytest.mark.negative
    async def test_get_user_posts_invalid_user(self, users_api):
        """Test getting posts for invalid user returns 200 or 404."""
        user_id = 99999
        response = await users_api.get_user_posts(user_id)
        # JSONPlaceholder returns empty array for non-existent users
        assert_status_code_in(response, [200, 404])

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, -1, "abc"])
    async def test_get_user_posts_with_invalid_ids(self, users_api, user_id):
        """Test getting posts with various invalid user IDs."""
        response = await users_api.get_user_posts(user_id)
        assert response.status in [200, 400, 404]

    @pytest.mark.critical
    async def test_user_posts_contain_required_fields(self, users_api):
        """Test all posts contain required fields."""
        user_id = 1
        response = await users_api.get_user_posts(user_id)
        assert_status_code(response, 200)
        
        data = await users_api.get_json(response)
        assert isinstance(data, list)
        
        for post in data:
            assert_response_field(post, "id")
            assert_response_field(post, "userId")
            assert_response_field(post, "title")
            assert_response_field(post, "body")


class TestUserPostsNegative:
    """Negative tests for Users API."""

    @pytest.mark.negative
    async def test_get_user_posts_with_special_characters(self, users_api):
        """Test getting user posts with special character user ID."""
        response = await users_api.get_user_posts("!@#$%")
        assert response.status in [200, 400, 404]

    @pytest.mark.negative
    async def test_get_user_posts_with_float_id(self, users_api):
        """Test getting user posts with float user ID."""
        response = await users_api.get_user_posts(1.5)
        assert response.status in [200, 400, 404]

    @pytest.mark.negative
    async def test_get_user_posts_boundary_values(self, users_api):
        """Test getting user posts with boundary values."""
        boundary_ids = [1, 10, 9999, -9999, 0]
        for user_id in boundary_ids:
            response = await users_api.get_user_posts(user_id)
            assert response.status in [200, 404]


class TestGetUserById:
    """Test GET /users/{id} endpoint."""

    @pytest.mark.critical
    async def test_get_user_by_id_returns_200(self, users_api):
        """Test GET /users/{id} with valid user ID returns 200."""
        user_id = 1
        response = await users_api.get_user_by_id(user_id)
        assert_status_code(response, 200)
        assert_content_type(response)
        assert_header_present(response, "content-type")

        data = await users_api.get_json(response)
        assert_response_field(data, "id")
        assert_response_field(data, "name")
        assert_response_field(data, "username")
        assert_response_field(data, "email")

    @pytest.mark.critical
    async def test_get_user_by_id_validates_schema(self, users_api):
        """Test GET /users/{id} response validates against UserSchema."""
        response = await users_api.get_user_by_id(1)
        assert_status_code(response, 200)

        data = await users_api.get_json(response)
        # Validate against Pydantic model
        user = UserSchema(**data)
        assert user.id == 1

    @pytest.mark.critical
    @pytest.mark.parametrize("user_id", [1, 5, 10])
    async def test_get_user_by_id_multiple_users(self, users_api, user_id):
        """Test GET /users/{id} for multiple valid users."""
        response = await users_api.get_user_by_id(user_id)
        assert_status_code(response, 200)

        data = await users_api.get_json(response)
        assert data.get("id") == user_id

    @pytest.mark.negative
    async def test_get_user_by_invalid_id_returns_404(self, users_api):
        """Test GET /users/{id} with invalid user ID returns 404."""
        response = await users_api.get_user_by_id(99999)
        assert_status_code_in(response, [404, 400])

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, -1, "abc"])
    async def test_get_user_by_id_invalid_formats(self, users_api, user_id):
        """Test GET /users/{id} with various invalid user ID formats."""
        response = await users_api.get_user_by_id(user_id)
        assert response.status in [200, 400, 404]

    @pytest.mark.critical
    async def test_get_user_by_id_contains_required_fields(self, users_api):
        """Test GET /users/{id} response contains all required fields."""
        response = await users_api.get_user_by_id(1)
        assert_status_code(response, 200)

        data = await users_api.get_json(response)
        assert_response_field(data, "id")
        assert_response_field(data, "name")
        assert_response_field(data, "username")
        assert_response_field(data, "email")
        # Ensure non-null constraints
        assert data["name"] != "", "User name should not be empty"
        assert data["username"] != "", "User username should not be empty"
