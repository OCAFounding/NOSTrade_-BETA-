from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import our routers
from api.signals.latest import router as signals_router
from api.signals.history import router as history_router
from api.strategy.endpoints import router as strategy_router
from api.agent.logs import router as logs_router

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NOS Trade API",
    description="API for NOS Trade trading system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(signals_router)
app.include_router(history_router)
app.include_router(strategy_router)
app.include_router(logs_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to NOS Trade API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 