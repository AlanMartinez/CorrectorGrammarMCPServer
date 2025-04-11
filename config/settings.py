import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token validation service
VALIDATE_TOKEN_URL = os.getenv("VALIDATE_TOKEN_URL", "http://localhost:8001/validate-token")

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mcp.db") 