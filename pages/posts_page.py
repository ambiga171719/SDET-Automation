"""Posts API Page Object."""

from pages.base_page import BasePage

POSTS_ENDPOINT = "/posts"


# Page Object for Posts API endpoints, inherits common API request methods from BasePage
class PostsPage(BasePage):
    """Page Object for Posts API endpoints."""

    # Specific methods for Posts API interactions - can be used in tests to perform actions related to posts

    async def get_all_posts(self, **kwargs):
        """Get all posts."""
        return await self.get(POSTS_ENDPOINT, **kwargs)

    async def get_post_by_id(self, post_id: int | str, **kwargs):
        """Get post by ID."""
        return await self.get(f"{POSTS_ENDPOINT}/{post_id}", **kwargs)

    async def get_posts_paginated(self, page: int, limit: int, **kwargs):
        """Get paginated posts."""
        return await self.get(
            f"{POSTS_ENDPOINT}?_page={page}&_limit={limit}",
            **kwargs
        )

    async def create_post(self, title: str, body: str, user_id: int, **kwargs):
        """Create new post."""

        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }

        return await self.post(
            POSTS_ENDPOINT,
            data=payload,
            **kwargs
        )

    async def update_post_full(
        self,
        post_id: int,
        title: str,
        body: str,
        user_id: int,
        **kwargs
    ):
        """Fully update post (PUT request)."""

        payload = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }

        return await self.put(
            f"{POSTS_ENDPOINT}/{post_id}",
            data=payload,
            **kwargs
        )

    async def update_post_partial(self, post_id: int, **kwargs):
        """Partially update post (PATCH request)."""
        return await self.patch(
            f"{POSTS_ENDPOINT}/{post_id}",
            data=kwargs
        )

    async def delete_post(self, post_id: int, **kwargs):
        """Delete post."""
        return await self.delete(
            f"{POSTS_ENDPOINT}/{post_id}",
            **kwargs
        )

    async def create_post_with_payload(self, payload: dict, **kwargs):
        """Create post with custom payload."""
        return await self.post(
            POSTS_ENDPOINT,
            data=payload,
            **kwargs
        )