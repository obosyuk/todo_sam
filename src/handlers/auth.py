"""
Authentication Lambda authorizer.

This module handles API Gateway Lambda authorization
using token-based authentication.
"""

import logging
import os
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_policy(effect: str, resource: str) -> Dict[str, Any]:
    """
    Create an IAM policy document.

    Args:
        effect: Allow or Deny
        resource: Resource ARN

    Returns:
        IAM policy document
    """
    return {
        "Version": "2012-10-17",
        "Statement": [
            {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
        ],
    }


def create_auth_response(
    principal_id: str, effect: str, resource: str
) -> Dict[str, Any]:
    """
    Create authorization response.

    Args:
        principal_id: Principal identifier
        effect: Allow or Deny
        resource: Resource ARN

    Returns:
        Authorization response dictionary
    """
    return {
        "principalId": principal_id,
        "policyDocument": create_policy(effect, resource),
    }


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

        # Get the secure token from environment variable
        auth_token = os.environ.get("AUTH_TOKEN")
        if not auth_token:
            logger.error("AUTH_TOKEN environment variable not set")
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
