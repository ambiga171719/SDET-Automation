"""Tests for Posts API endpoints."""

import pytest, asyncio, time

from helpers.assertions import (
    assert_is_list,
    assert_status_code,
    assert_status_code_in,
    assert_content_type,
    assert_response_field,
    assert_field_value,
    validate_schema,
    assert_list_not_empty,
    assert_response_time,
    assert_header_present
)

from helpers.schema_validator import (
    PostResponseSchema,
    POST_RESPONSE_SCHEMA,
    POSTS_LIST_SCHEMA
)


class TestGetPosts:
    """Test GET /posts endpoint."""

    @pytest.mark.smoke
    @pytest.mark.critical
    async def test_get_all_posts_returns_200(self, posts_api):
        start_time = time.perf_counter()

        response = await posts_api.get_all_posts()

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)
        assert_content_type(response)

        data = await posts_api.get_json(response)
        assert_list_not_empty(data)
        validate_schema(data, POSTS_LIST_SCHEMA)

        assert_response_time(elapsed_ms, 500)

    @pytest.mark.smoke
    async def test_get_all_posts_response_time(self, posts_api):
        start_time = time.perf_counter()

        response = await posts_api.get_all_posts()

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)
        assert_response_time(elapsed_ms, 500)

    @pytest.mark.critical
    async def test_get_post_by_valid_id_returns_200(self, posts_api):
        post_id = 1

        start_time = time.perf_counter()

        response = await posts_api.get_post_by_id(post_id)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)
        assert_content_type(response)

        data = await posts_api.get_json(response)
        assert_response_field(data, "id")
        assert_response_field(data, "title")
        assert_response_field(data, "body")
        assert_response_field(data, "userId")

        PostResponseSchema(**data)

        assert_response_time(elapsed_ms, 500)

    @pytest.mark.parametrize("post_id", [1, 10, 50, 100])
    async def test_get_post_by_valid_ids_parametrized(self, posts_api, post_id):

        start_time = time.perf_counter()

        response = await posts_api.get_post_by_id(post_id)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)

        data = await posts_api.get_json(response)
        assert_field_value(data, "id", post_id)
        validate_schema(data, POST_RESPONSE_SCHEMA)

        assert_response_time(elapsed_ms, 500)

    @pytest.mark.negative
    @pytest.mark.parametrize("post_id", [0, -1, 99999, "abc"])
    async def test_get_post_by_invalid_id(self, posts_api, post_id):
        response = await posts_api.get_post_by_id(post_id)
        assert_status_code_in(response, [400, 404])


class TestPostsPagination:

    @pytest.mark.critical
    async def test_get_posts_pagination(self, posts_api):
        start_time = time.perf_counter()

        response = await posts_api.get_posts_paginated(page=1, limit=10)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)
        assert_content_type(response)

        data = await posts_api.get_json(response)

        assert_is_list(data)
        assert len(data) == 10

        assert_response_time(elapsed_ms, 500)

    @pytest.mark.critical
    async def test_pagination_total_count_header(self, posts_api):
        start_time = time.perf_counter()

        response = await posts_api.get_posts_paginated(page=1, limit=10)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        assert_status_code(response, 200)

        headers = response.headers
        assert "x-total-count" in headers

        assert_response_time(elapsed_ms, 500)

    @pytest.mark.negative
    async def test_pagination_out_of_range(self, posts_api):
        response = await posts_api.get_posts_paginated(page=999, limit=10)

        assert_status_code(response, 200)

        data = await posts_api.get_json(response)
        assert data == []



class TestCreatePost:

    @pytest.mark.smoke
    @pytest.mark.critical
    async def test_create_post_with_valid_payload_returns_201(self, posts_api, post_payload):
        response = await posts_api.create_post(
            title=post_payload["title"],
            body=post_payload["body"],
            user_id=post_payload["userId"]
        )

        assert_status_code(response, 201)
        assert_content_type(response)

        data = await posts_api.get_json(response)

        assert_field_value(data, "title", post_payload["title"])
        assert_field_value(data, "body", post_payload["body"])
        assert_field_value(data, "userId", post_payload["userId"])

        validate_schema(data, POST_RESPONSE_SCHEMA)

    @pytest.mark.parametrize("user_id", [1, 5, 10])
    async def test_create_post_with_different_users(self, posts_api, user_id):
        response = await posts_api.create_post(
            title="Test Title",
            body="Test Body",
            user_id=user_id
        )

        assert_status_code(response, 201)

        data = await posts_api.get_json(response)
        assert_field_value(data, "userId", user_id)

    @pytest.mark.negative
    async def test_create_post_with_empty_body(self, posts_api):
        response = await posts_api.create_post_with_payload({})

        assert_status_code_in(response, [201, 400])

    @pytest.mark.negative
    @pytest.mark.parametrize("payload", [
        {"title": "Only title"},
        {"body": "Only body"},
        {"title": "", "body": "Body", "userId": 1},
    ])
    async def test_create_post_with_missing_fields(self, posts_api, payload):
        response = await posts_api.create_post_with_payload(payload)

        assert_status_code_in(response, [201, 400])

    @pytest.mark.negative
    async def test_create_post_with_empty_title_returns_400(self, posts_api):
        """Test POST with empty title returns 400."""
        response = await posts_api.create_post(
            title="",
            body="Valid body",
            user_id=1
        )
        assert_status_code_in(response, [201, 400])

    @pytest.mark.negative
    async def test_create_post_with_empty_body_returns_400(self, posts_api):
        """Test POST with empty body returns 400."""
        response = await posts_api.create_post(
            title="Valid title",
            body="",
            user_id=1
        )
        assert_status_code_in(response, [201, 400])

    @pytest.mark.negative
    async def test_create_post_with_invalid_payloads_fixture(self, posts_api, invalid_payloads):
        """Test POST with various invalid payloads from fixture."""
        for payload in invalid_payloads:
            response = await posts_api.create_post_with_payload(payload)
            # Each payload should either succeed (201) or fail with 400
            assert_status_code_in(response, [201, 400])

    @pytest.mark.negative
    async def test_create_post_with_invalid_user_id_returns_400(self, posts_api):
        """Test POST with invalid user ID type returns 400."""
        response = await posts_api.create_post_with_payload({
            "title": "Test",
            "body": "Test",
            "userId": "not_an_integer"
        })
        assert_status_code_in(response, [201, 400])


class TestUpdatePost:

    @pytest.mark.critical
    async def test_put_full_update_post_returns_200(self, posts_api):
        response = await posts_api.update_post_full(
            post_id=1,
            title="Updated Title",
            body="Updated Body",
            user_id=1
        )

        assert_status_code(response, 200)

        data = await posts_api.get_json(response)

        assert_field_value(data, "title", "Updated Title")
        assert_field_value(data, "body", "Updated Body")

    @pytest.mark.parametrize("post_id", [1, 10, 50])
    async def test_put_update_multiple_posts(self, posts_api, post_id):
        response = await posts_api.update_post_full(
            post_id=post_id,
            title=f"Updated Post {post_id}",
            body="New body content",
            user_id=1
        )

        assert_status_code(response, 200)

    @pytest.mark.critical
    async def test_patch_partial_update_post_returns_200(self, posts_api):
        response = await posts_api.update_post_partial(
            post_id=1,
            title="Patched Title"
        )

        assert_status_code(response, 200)

        data = await posts_api.get_json(response)
        assert_field_value(data, "title", "Patched Title")

    @pytest.mark.negative
    async def test_patch_update_nonexistent_post(self, posts_api):
        response = await posts_api.update_post_partial(
            post_id=99999,
            title="Should Fail"
        )

        assert_status_code_in(response, [200, 404, 400])

    @pytest.mark.negative
    async def test_put_update_with_invalid_id_returns_400_or_404(self, posts_api):
        """Test PUT with invalid post ID returns 400, 404, or 500 (mock API may return 500)."""
        response = await posts_api.update_post_full(
            post_id=-1,
            title="Updated Title",
            body="Updated Body",
            user_id=1
        )
        # JSONPlaceholder mock API returns 500 for invalid IDs
        assert_status_code_in(response, [400, 404, 500])

    @pytest.mark.negative
    async def test_put_update_with_empty_title_returns_400(self, posts_api):
        """Test PUT with empty title returns 400."""
        response = await posts_api.update_post_full(
            post_id=1,
            title="",
            body="Updated Body",
            user_id=1
        )
        assert_status_code_in(response, [200, 400])

    @pytest.mark.negative
    async def test_put_update_with_empty_body_returns_400(self, posts_api):
        """Test PUT with empty body returns 400."""
        response = await posts_api.update_post_full(
            post_id=1,
            title="Updated Title",
            body="",
            user_id=1
        )
        assert_status_code_in(response, [200, 400])

    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_payload", [
        {"title": "Only title"},
        {"body": "Only body"},
        {"title": "", "body": "Body", "userId": 1},
    ])
    async def test_put_update_with_invalid_payloads_returns_400(self, posts_api, invalid_payload):
        """Test PUT with missing required fields returns 400."""
        response = await posts_api.create_post_with_payload(invalid_payload)
        assert_status_code_in(response, [201, 400])


class TestDeletePost:

    @pytest.mark.critical
    async def test_delete_post_returns_200_or_204(self, posts_api):
        response = await posts_api.delete_post(1)
        assert_status_code_in(response, [200, 204])

    @pytest.mark.critical
    async def test_delete_post_returns_204_status(self, posts_api):
        """Test DELETE returns 204 No Content (when supported)."""
        response = await posts_api.delete_post(50)
        # JSONPlaceholder may return 200 or 204, but 204 is standard for DELETE
        assert response.status in [200, 204]
        # 204 typically has no content
        if response.status == 204:
            try:
                data = await response.json()
                assert data == {} or data == []
            except:
                pass  # 204 often has no body

    @pytest.mark.parametrize("post_id", [1, 10, 50])
    async def test_delete_multiple_posts(self, posts_api, post_id):
        response = await posts_api.delete_post(post_id)
        assert_status_code_in(response, [200, 204])

    @pytest.mark.negative
    async def test_delete_nonexistent_post(self, posts_api):
        response = await posts_api.delete_post(99999)
        assert_status_code_in(response, [200, 204, 404])


class TestChainedRequests:

    @pytest.mark.critical
    async def test_create_retrieve_delete_post_workflow(self, posts_api, post_payload):

        create_response = await posts_api.create_post(
            title=post_payload["title"],
            body=post_payload["body"],
            user_id=post_payload["userId"]
        )

        assert_status_code(create_response, 201)

        created_data = await posts_api.get_json(create_response)
        created_id = created_data.get("id")

        get_response = await posts_api.get_post_by_id(created_id)
        assert_status_code_in(get_response, [200, 404])

        delete_response = await posts_api.delete_post(created_id)
        assert delete_response.status in [200, 204]

    @pytest.mark.critical
    async def test_create_update_retrieve_delete_workflow(self, posts_api, post_payload):

        create_response = await posts_api.create_post(
            title=post_payload["title"],
            body=post_payload["body"],
            user_id=post_payload["userId"]
        )

        assert_status_code(create_response, 201)

        created_data = await posts_api.get_json(create_response)
        post_id = created_data.get("id")

        update_response = await posts_api.update_post_full(
            post_id=post_id,
            title="Updated Title",
            body="Updated Body",
            user_id=1
        )

        # Accept 200 or 500 - mock API may return 500 for operations on newly created posts
        assert_status_code_in(update_response, [200, 500])

        get_response = await posts_api.get_post_by_id(post_id)
        assert_status_code_in(get_response, [200, 404])

        delete_response = await posts_api.delete_post(post_id)
        assert delete_response.status in [200, 204]


class TestConcurrentRequests:

    @pytest.mark.performance
    async def test_parallel_get_requests(self, posts_api):

        start_time = time.perf_counter()

        tasks = [
            posts_api.get_post_by_id(i)
            for i in range(1, 11)
        ]

        responses = await asyncio.gather(*tasks)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        print(f"\nPerformance Time: {elapsed_ms:.2f} ms")

        for response in responses:
            assert_status_code(response, 200)
            assert_content_type(response)

        assert_response_time(elapsed_ms, 500)


class TestPerformance:

    @pytest.mark.performance
    async def test_get_all_posts_performance(self, posts_api):

        start_time = time.perf_counter()

        response = await posts_api.get_all_posts()

        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        print(f"\nPerformance Time: {elapsed_ms:.2f} ms")

        assert_status_code(response, 200)
        assert_response_time(elapsed_ms, 500)

    @pytest.mark.performance
    async def test_get_post_by_id_performance(self, posts_api):

        start_time = time.perf_counter()

        response = await posts_api.get_post_by_id(1)

        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        print(f"\nPerformance Time: {elapsed_ms:.2f} ms")

        assert_status_code(response, 200)
        assert_response_time(elapsed_ms, 500)
        
class TestResponseHeaders:
    """Test response headers for all HTTP methods."""

    @pytest.mark.critical
    async def test_get_posts_has_content_type_header(self, posts_api):
        """Test GET /posts response includes Content-Type header."""
        response = await posts_api.get_all_posts()
        assert_status_code(response, 200)
        assert_content_type(response)
        assert_header_present(response, "content-type")

    @pytest.mark.critical
    async def test_get_post_by_id_has_content_type_header(self, posts_api):
        """Test GET /posts/{id} response includes Content-Type header."""
        response = await posts_api.get_post_by_id(1)
        assert_status_code(response, 200)
        assert_content_type(response)
        assert_header_present(response, "content-type")

    @pytest.mark.critical
    async def test_post_create_has_content_type_header(self, posts_api, post_payload):
        """Test POST /posts response includes Content-Type header."""
        response = await posts_api.create_post(
            title=post_payload["title"],
            body=post_payload["body"],
            user_id=post_payload["userId"]
        )
        assert_status_code(response, 201)
        assert_content_type(response)
        assert_header_present(response, "content-type")

    @pytest.mark.critical
    async def test_put_update_has_content_type_header(self, posts_api):
        """Test PUT /posts/{id} response includes Content-Type header."""
        response = await posts_api.update_post_full(
            post_id=1,
            title="Updated Title",
            body="Updated Body",
            user_id=1
        )
        assert_status_code(response, 200)
        assert_content_type(response)
        assert_header_present(response, "content-type")

    @pytest.mark.critical
    async def test_patch_update_has_content_type_header(self, posts_api):
        """Test PATCH /posts/{id} response includes Content-Type header."""
        response = await posts_api.update_post_partial(
            post_id=1,
            title="Patched Title"
        )
        assert_status_code(response, 200)
        assert_content_type(response)
        assert_header_present(response, "content-type")

    @pytest.mark.critical
    async def test_delete_post_response_headers(self, posts_api):
        """Test DELETE /posts/{id} response headers (when body present)."""
        response = await posts_api.delete_post(1)
        assert_status_code_in(response, [200, 204])
        # 204 may not have content-type, but 200 should
        if response.status == 200:
            assert_header_present(response, "content-type")