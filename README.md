# Condor Todo API

A serverless todo application built with AWS SAM, Python, and DynamoDB, featuring token-based authentication.

## 🚀 Features

- **RESTful API** for todo management (create action only)
- **Token-based authentication** using Lambda authorizers (simple authentication with saved auth token in SSM Parameter Store, suitable for server-to-server communication)
- **Data validation** with Pydantic models
- **Structured logging** for monitoring
- **Error handling** with standardized responses
- **CORS support** for web applications

## 📋 Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Python 3.13+

## 🛠️ Development

### Local Testing

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Deployment

```bash
# Build the application
sam build

# Deploy with guided setup
sam deploy --guided

# Update the auth token in SSM Parameter Store (after deployment)
aws ssm put-parameter \
  --name "/condor-todo-app/auth-token" \
  --value "your-secure-token" \
  --type "SecureString" \
  --overwrite
```

### API Usage

```bash
# Get the API endpoint from CloudFormation outputs
API_URL=$(aws cloudformation describe-stacks \
  --stack-name condor-sam-todo-app \
  --query 'Stacks[0].Outputs[?OutputKey==`TodoApiUrl`].OutputValue' \
  --output text)

# Create a todo item (use the token you set in SSM)
curl -X POST "$API_URL" \
  -H "Authorization: Bearer your-secure-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "Remember to buy milk"}'
```

## 🔧 Configuration

### Environment Variables

- `AUTH_TOKEN_PARAMETER_NAME`: SSM Parameter name containing the authentication token
- `TABLE_NAME`: DynamoDB table name for todos
- `LOG_LEVEL`: Logging level (default: INFO)

### SSM Parameters

- `/condor-todo-app/auth-token`: Encrypted authentication token for API access

## 📊 Monitoring

The application provides extensive logging and performance monitoring via CloudWatch (log groups and metrics)

## 🔒 Security

- Token-based authentication with encrypted SSM parameter storage
- IAM roles with least privilege
- Input validation with Pydantic
- CORS configuration
