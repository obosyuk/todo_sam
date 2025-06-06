# Condor Todo API

A serverless todo application built with AWS SAM, Python, and DynamoDB, featuring token-based authentication.

## 🚀 Features

- **RESTful API** for todo management
- **Token-based authentication** using Lambda authorizers
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
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run specific test
python -m unittest tests.test_todo_handler.TestTodoHandler.test_create_todo_success
```

### Deployment

```bash
# Build the application
sam build

# Deploy with guided setup
sam deploy --guided

# Deploy with custom token
sam deploy --parameter-overrides AuthToken="your-secure-token"
```

### API Usage

```bash
# Get the API endpoint from CloudFormation outputs
API_URL=$(aws cloudformation describe-stacks \
  --stack-name condor-sam-todo-app \
  --query 'Stacks[0].Outputs[?OutputKey==`TodoApiUrl`].OutputValue' \
  --output text)

# Create a todo item
curl -X POST "$API_URL" \
  -H "Authorization: Bearer your-secure-token" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "Remember to buy milk"}'
```

## 🔧 Configuration

### Environment Variables

- `AUTH_TOKEN`: Authentication token for API access
- `TABLE_NAME`: DynamoDB table name for todos
- `LOG_LEVEL`: Logging level (default: INFO)

### SAM Parameters

- `AuthToken`: Secure token for API authentication (NoEcho)

## 📊 Monitoring

The application includes structured logging for monitoring:

- Request/response logging
- Error tracking with stack traces
- Performance metrics via CloudWatch

## 🔒 Security

- Token-based authentication
- IAM roles with least privilege
- Input validation with Pydantic
- CORS configuration
- No hardcoded secrets

## 🧪 Testing

The project includes comprehensive tests:

- Unit tests for handlers
- Mocked AWS services
- Error case coverage
- Validation testing

Run tests with:
```bash
python -m pytest tests/ -v
``` 