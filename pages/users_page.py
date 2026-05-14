"""Users API Page Object."""
from pages.base_page import BasePage

# Page Object for Users API endpoints, inherits common API request methods from BasePage
class UsersPage(BasePage):
    """Page Object for Users API endpoints."""

# Specific methods for Users API interactions - can be used in tests to perform actions related to users
    async def get_user_posts(self, user_id: int, **kwargs):
        """Get all posts for a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            APIResponse
        """
        return await self.get(f"/users/{user_id}/posts", **kwargs)

# Get user by ID - useful for testing retrieval of user details
    async def get_user_by_id(self, user_id: int, **kwargs):
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            APIResponse
        """
        return await self.get(f"/users/{user_id}", **kwargs)
