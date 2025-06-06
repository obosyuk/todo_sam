"""
Todo API Lambda handler.

This module handles HTTP requests for todo item operations
"""

import json
import logging
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from pydantic import ValidationError

from src.models.todo import TodoItem
from src.utils.response import (
    success_response,
    error_response,
    validation_error_response,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("TABLE_NAME")
if not table_name:
    raise ValueError("TABLE_NAME environment variable is required")
table = dynamodb.Table(table_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle HTTP requests for todo operations.

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        HTTP response dictionary
    """
    try:
        logger.info(
            f"Processing request: {event.get('httpMethod')} {event.get('path')}"
        )

        if not event.get("body"):
            return error_response("Request body is required", 400)

        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request body: {e}")
            return error_response("Invalid JSON format", 400)

        try:
            todo_item = TodoItem(**body)
        except ValidationError as ve:
            logger.warning(f"Validation error: {ve.errors()}")
            return validation_error_response(ve.errors())

        try:
            table.put_item(Item=todo_item.model_dump())
            logger.info(f"Created todo item with ID: {todo_item.id}")

            return success_response(
                data={"id": todo_item.id, "title": todo_item.title},
                message="Todo item created successfully",
            )

        except ClientError as e:
            logger.error(f"DynamoDB error: {e}")
            return error_response("Failed to save todo item", 500)

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return error_response("Internal server error", 500)
