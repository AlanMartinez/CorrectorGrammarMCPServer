# Model Context Protocol (MCP) Server

A FastAPI-based server that provides text correction services using OpenAI's GPT models. This server implements a clean architecture pattern with proper separation of concerns.

## Project Structure

```
MCPServer/
├── config/              # Configuration files
│   ├── __init__.py
│   └── settings.py      # Application settings
├── models/             # Data models
│   ├── __init__.py
│   └── input_model.py  # Input data models
├── routes/             # API routes
│   ├── __init__.py
│   └── text_routes.py  # Text-related endpoints
├── services/           # Business logic
│   ├── __init__.py
│   └── openai_service.py  # OpenAI integration
├── .env               # Environment variables
├── requirements.txt   # Project dependencies
├── README.md         # Documentation
└── server.py         # Application entry point
```

## Features

- Text correction using OpenAI's GPT models
- Clean architecture implementation
- Error handling and logging
- Configuration management
- API versioning
- RESTful API endpoints

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- OpenAI API key

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python server.py
```

The server will start on `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Text Correction

- `POST /api/v1/correct` - Correct text using OpenAI's GPT model

Example request:
```bash
curl -X POST "http://localhost:8000/api/v1/correct" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "i am going to the store"
         }'
```

Example response:
```json
{
    "corrected": "I am going to the store."
}
```

Error response example:
```json
{
    "error": "API quota exceeded",
    "message": "The OpenAI API quota has been exceeded. Please check your billing details or try again later.",
    "details": "Visit https://platform.openai.com/account/billing to check your quota and billing status."
}
```

## Configuration

The application can be configured through the following settings in `config/settings.py`:

- `OPENAI_MODEL`: The OpenAI model to use (default: "gpt-3.5-turbo")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: "INFO")

## Error Handling

The server includes comprehensive error handling for:
- OpenAI API errors
- Quota exceeded errors
- Invalid input errors
- Server errors

All errors are logged and return appropriate HTTP status codes with detailed error messages.

## Development

To extend the server with new features:

1. Add new models in the `models/` directory
2. Create new services in the `services/` directory
3. Add new routes in the `routes/` directory
4. Update configuration in `config/settings.py` if needed

## Security Note

Make sure to:
- Keep your API keys secure
- Never commit the `.env` file to version control
- Use appropriate rate limiting in production
- Implement proper authentication if needed 