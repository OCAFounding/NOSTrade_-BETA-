from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
from pydantic import BaseModel
import time
from datetime import datetime

# Import our components
from signal_router import SignalRouter
from ai_agent_parent import ParentAI
from trading_bot_executor import TradeExecutor

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create router
router = APIRouter()

# Initialize components
signal_router = SignalRouter()
parent_ai = ParentAI()
trade_executor = TradeExecutor()

class LogEntry(BaseModel):
    """Model for a log entry"""
    timestamp: str
    message: str
    level: str = "info"  # info, warning, error
    source: str = "system"  # system, ai, trade

class LogsResponse(BaseModel):
    """Response model for logs endpoint"""
    logs: List[LogEntry]
    count: int

# In-memory log storage (in production, use a proper database)
log_storage = []

def add_log(message: str, level: str = "info", source: str = "system"):
    """
    Add a log entry to the storage.
    
    Args:
        message: Log message
        level: Log level (info, warning, error)
        source: Log source (system, ai, trade)
    """
    log_entry = LogEntry(
        timestamp=datetime.now().isoformat(),
        message=message,
        level=level,
        source=source
    )
    log_storage.append(log_entry)
    
    # Trim logs if too many
    if len(log_storage) > 1000:
        log_storage.pop(0)
        
@router.get("/api/agent/logs", response_model=LogsResponse)
async def get_logs(
    limit: int = 100,
    level: str = None,
    source: str = None
):
    """
    Get AI agent coordination logs.
    
    Args:
        limit: Maximum number of logs to return (default: 100)
        level: Filter logs by level (info, warning, error)
        source: Filter logs by source (system, ai, trade)
        
    Returns:
        LogsResponse: List of log entries
    """
    try:
        # Get logs from storage
        logs = log_storage.copy()
        
        # Apply filters
        if level:
            logs = [log for log in logs if log.level == level]
        if source:
            logs = [log for log in logs if log.source == source]
            
        # Apply limit
        logs = logs[-limit:]
        
        return LogsResponse(
            logs=logs,
            count=len(logs)
        )
        
    except Exception as e:
        logger.error(f"Error getting logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
# Add some initial logs
add_log("System initialized", "info", "system")
add_log("AI agent started", "info", "ai")
add_log("Trade executor ready", "info", "trade") 