"""
Authentication Lambda authorizer.

This module handles API Gateway Lambda authorization
using token-based authentication.
"""

import logging
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ssm_client = boto3.client("ssm")


def create_policy(effect: str, resource: str) -> Dict[str, Any]:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
        ],
    }


def create_auth_response(
    principal_id: str, effect: str, resource: str
) -> Dict[str, Any]:
    return {
        "principalId": principal_id,
        "policyDocument": create_policy(effect, resource),
    }


def get_auth_token_from_ssm() -> str:
    """
    Retrieve the auth token from SSM Parameter Store.

    Returns:
        Auth token string

    Raises:
        ValueError: If parameter name is not configured or token cannot be retrieved
    """
    parameter_name = os.environ.get("AUTH_TOKEN_PARAMETER_NAME")
    if not parameter_name:
        raise ValueError("AUTH_TOKEN_PARAMETER_NAME environment variable not set")

    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ClientError as e:
        logger.error(f"Failed to retrieve auth token from SSM: {e}")
        raise ValueError(f"Failed to retrieve auth token: {e}")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle API Gateway authorization requests.

    Args:
        event: API Gateway authorizer event
        context: Lambda context

    Returns:
        Authorization response
    """
    try:
        token = event.get("authorizationToken")
        method_arn = event.get("methodArn")

        if not token or not method_arn:
            logger.warning("Missing authorization token or method ARN")
            return create_auth_response("unauthorized", "Deny", method_arn or "*")

        logger.info("Processing authorization request")

        # Get the secure token from SSM Parameter Store
        try:
            auth_token = get_auth_token_from_ssm()
        except ValueError as e:
            logger.error(f"Failed to get auth token: {e}")
            return create_auth_response("unauthorized", "Deny", method_arn)

        if token == auth_token:
            logger.info("Authorization successful")
            return create_auth_response("user", "Allow", method_arn)
        else:
            logger.warning("Invalid authorization token")
            return create_auth_response("unauthorized", "Deny", method_arn)

    except Exception as e:
        logger.error(f"Authorization error: {e}", exc_info=True)
        return create_auth_response("unauthorized", "Deny", event.get("methodArn", "*"))
