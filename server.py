from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from config.settings import HOST, PORT, LOG_LEVEL
from routes.text_routes import router as text_router

# Configure logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="MCP Server", description="Model Context Protocol Server")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(text_router, prefix="/api/v1", tags=["text"])

if __name__ == "__main__":
    logger.info("Starting MCP Server...")
    uvicorn.run(app, host=HOST, port=PORT) 