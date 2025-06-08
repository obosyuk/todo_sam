"""
Todo item data model with validation.

This module defines the TodoItem Pydantic model for validating
and serializing todo items in the API.
"""

from typing import Optional
import uuid

from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    completed: bool = Field(default=False)
