import json
import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

from src.handlers.todo import lambda_handler


@pytest.fixture
def context():
    """Lambda context fixture."""
    return MagicMock()


@patch("src.handlers.todo.table")
def test_create_todo_success(mock_table, context):
    mock_table.put_item.return_value = {}

    event = {
        "httpMethod": "POST",
        "path": "/todo",
        "body": json.dumps(
            {"title": "Buy milk", "description": "Remember to buy milk"}
        ),
    }

    response = lambda_handler(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert response_body["message"] == "Todo item created successfully"
    assert "id" in response_body["data"]
    assert response_body["data"]["title"] == "Buy milk"


def test_create_todo_missing_title(context):
    event = {
        "httpMethod": "POST",
        "path": "/todo",
        "body": json.dumps({"description": "No title provided"}),
    }

    response = lambda_handler(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["error"] == "Validation failed"
    assert "details" in response_body


def test_create_todo_empty_body(context):
    event = {"httpMethod": "POST", "path": "/todo", "body": None}

    response = lambda_handler(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["error"] == "Request body is required"


def test_create_todo_invalid_json(context):
    event = {"httpMethod": "POST", "path": "/todo", "body": "invalid json"}

    response = lambda_handler(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["error"] == "Invalid JSON format"


@patch("src.handlers.todo.table")
def test_create_todo_dynamodb_error(mock_table, context):
    mock_table.put_item.side_effect = ClientError(
        error_response={"Error": {"Code": "ValidationException"}},
        operation_name="PutItem",
    )

    event = {
        "httpMethod": "POST",
        "path": "/todo",
        "body": json.dumps({"title": "Test todo"}),
    }

    response = lambda_handler(event, context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert response_body["error"] == "Failed to save todo item"
