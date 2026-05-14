from pydantic import BaseModel, ConfigDict, Field

# Pydantic models for validating API response data - can be used in tests to ensure response structure and types are correct
class PostCreateSchema(BaseModel):
    userId: int
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="allow")


class PostResponseSchema(BaseModel):
    userId: int
    id: int
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="allow")

# Schema for list of posts - useful for validating responses that return multiple posts
class UserSchema(BaseModel):
    """Schema for User object."""
    id: int
    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    email: str

    model_config = ConfigDict(extra="allow")


# JSON Schema definitions
POST_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string", "minLength": 1}
    },
    "required": ["userId", "id", "title", "body"]
}
# Schema for list of posts - useful for validating responses that return multiple posts
POSTS_LIST_SCHEMA = {
    "type": "array",
    "items": POST_RESPONSE_SCHEMA
}

# Schema for list of posts for a user - similar to POSTS_LIST_SCHEMA but can be used specifically for user posts endpoint 

USER_POSTS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "userId": {"type": "integer"},
            "id": {"type": "integer"},
            "title": {"type": "string", "minLength": 1},
            "body": {"type": "string", "minLength": 1}
        },
        "required": ["userId", "id", "title", "body"]
    }
}
