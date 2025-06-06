"""
Tests for the todo handler module.

This module contains unit tests for the todo API Lambda handler
with proper mocking and error case coverage.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from src.handlers.todo import lambda_handler


class TestTodoHandler(unittest.TestCase):
    """Test cases for the todo Lambda handler."""

    def setUp(self):
        """Set up test fixtures."""
        self.context = MagicMock()

    @patch("src.handlers.todo.table")
    def test_create_todo_success(self, mock_table):
        """Test successful todo item creation."""
        mock_table.put_item.return_value = {}

        event = {
            "httpMethod": "POST",
            "path": "/todo",
            "body": json.dumps(
                {"title": "Buy milk", "description": "Remember to buy milk"}
            ),
        }

        response = lambda_handler(event, self.context)
        response_body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response_body["message"], "Todo item created successfully")
        self.assertIn("id", response_body["data"])
        self.assertEqual(response_body["data"]["title"], "Buy milk")

    def test_create_todo_missing_title(self):
        """Test todo creation with missing required title."""
        event = {
            "httpMethod": "POST",
            "path": "/todo",
            "body": json.dumps({"description": "No title provided"}),
        }

        response = lambda_handler(event, self.context)
        response_body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response_body["error"], "Validation failed")
        self.assertIn("details", response_body)

    def test_create_todo_empty_body(self):
        """Test todo creation with empty request body."""
        event = {"httpMethod": "POST", "path": "/todo", "body": None}

        response = lambda_handler(event, self.context)
        response_body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response_body["error"], "Request body is required")

    def test_create_todo_invalid_json(self):
        """Test todo creation with invalid JSON."""
        event = {"httpMethod": "POST", "path": "/todo", "body": "invalid json"}

        response = lambda_handler(event, self.context)
        response_body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(response_body["error"], "Invalid JSON format")

    @patch("src.handlers.todo.table")
    def test_create_todo_dynamodb_error(self, mock_table):
        """Test todo creation with DynamoDB error."""
        from botocore.exceptions import ClientError

        mock_table.put_item.side_effect = ClientError(
            error_response={"Error": {"Code": "ValidationException"}},
            operation_name="PutItem",
        )

        event = {
            "httpMethod": "POST",
            "path": "/todo",
            "body": json.dumps({"title": "Test todo"}),
        }

        response = lambda_handler(event, self.context)
        response_body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 500)
        self.assertEqual(response_body["error"], "Failed to save todo item")


if __name__ == "__main__":
    unittest.main()
