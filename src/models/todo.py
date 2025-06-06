"""
Todo item data model with validation.

This module defines the TodoItem Pydantic model for validating
and serializing todo items in the API.
"""

from typing import Optional
import uuid

from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    """
    Represents a Todo item with validation.

    Attributes:
        id: Unique identifier for the todo item (auto-generated)
        title: The title of the todo item (required, 1-100 chars)
        description: Optional description (max 255 chars)
        completed: Whether the todo item is completed
    """

    id: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the todo item",
    )
    title: str = Field(
        ..., min_length=1, max_length=100, description="Title of the TODO item"
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Optional description of the todo item"
    )
    completed: bool = Field(
        default=False, description="Whether the todo item is completed"
    )
