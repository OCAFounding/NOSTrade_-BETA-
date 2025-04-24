import asyncio
import signal
import os
import threading
from orchestrator import Orchestrator
from ai_agents.parent_agent import ParentAgent
from ai_agents.child_agent import ChildAgent
from ai_agents.strategies import STRATEGIES
from feeds.signal_processor import SignalProcessor
from utils.logger import logger
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

# Import routers
from api.stress import router as stress_router
from api.ai_chat import router as ai_chat_router
# Import other routers as they are created
# from api.monitoring import router as monitoring_router
# from api.compliance import router as compliance_router

# Create FastAPI app
app = FastAPI(
    title="NOS Trade API",
    description="API for the NOS Trade multi-agent trading system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stress_router)
app.include_router(ai_chat_router)
# Include other routers as they are created
# app.include_router(monitoring_router)
# app.include_router(compliance_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to NOS Trade API"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

async def setup_ai_agents():
    """
    Set up the AI agent hierarchy
    """
    # Create child agents for different assets
    btc_agent = ChildAgent("BTC")
    eth_agent = ChildAgent("ETH")
    forex_agent = ChildAgent("EUR/USD")
    
    # Add strategies to each agent
    for agent in [btc_agent, eth_agent, forex_agent]:
        for strategy_name, strategy_fn in STRATEGIES.items():
            agent.add_strategy(strategy_name, strategy_fn)
    
    # Create parent agent
    parent_agent = ParentAgent([btc_agent, eth_agent, forex_agent])
    
    return parent_agent

def start_price_feed_server():
    """
    Start the price feed server in a separate process
    """
    import subprocess
    import sys
    
    # Start the Node.js server
    node_process = subprocess.Popen(
        ["node", "feeds/price_feed_server.js"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    logger.info("Started price feed server")
    return node_process

async def main():
    # Create logs and data directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Start the price feed server
    node_process = start_price_feed_server()
    
    # Create orchestrator
    orchestrator = Orchestrator()
    
    # Set up AI agents
    parent_agent = await setup_ai_agents()
    
    # Create signal processor
    signal_processor = SignalProcessor(parent_agent)
    
    # Handle shutdown signals
    def handle_shutdown(signum, frame):
        logger.info("Shutdown signal received. Cleaning up...")
        signal_processor.stop()
        asyncio.create_task(orchestrator.cleanup())
        node_process.terminate()
    
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        # Start the trading system
        logger.info("Starting NOS Trade system...")
        await orchestrator.start()
        
        # Start the signal processor
        signal_processor.start()
        
        # Keep the main loop running
        while orchestrator.running:
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}")
        signal_processor.stop()
        await orchestrator.cleanup()
        node_process.terminate()
        raise

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 