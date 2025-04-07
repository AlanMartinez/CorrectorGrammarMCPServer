import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000

# Logging Configuration
LOG_LEVEL = "INFO" 