from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
from pydantic import BaseModel
from datetime import datetime
import time

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

class ComplianceLog(BaseModel):
    """Model for a compliance log entry"""
    timestamp: str
    message: str
    level: str = "info"  # info, warning, error, violation
    category: str = "general"  # general, risk, trade, position, leverage
    details: Dict[str, Any] = {}

class ComplianceLogsResponse(BaseModel):
    """Response model for compliance logs endpoint"""
    logs: List[ComplianceLog]
    count: int

# In-memory compliance log storage (in production, use a proper database)
compliance_logs = []

def add_compliance_log(
    message: str,
    level: str = "info",
    category: str = "general",
    details: Dict[str, Any] = {}
):
    """
    Add a compliance log entry to the storage.
    
    Args:
        message: Log message
        level: Log level (info, warning, error, violation)
        category: Log category (general, risk, trade, position, leverage)
        details: Additional details about the log entry
    """
    log_entry = ComplianceLog(
        timestamp=datetime.now().isoformat(),
        message=message,
        level=level,
        category=category,
        details=details
    )
    compliance_logs.append(log_entry)
    
    # Trim logs if too many (keep last 1000 entries)
    if len(compliance_logs) > 1000:
        compliance_logs.pop(0)
        
    # Log to system logger
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.log(log_level, f"Compliance [{category}]: {message}")

@router.get("/api/compliance/logs", response_model=ComplianceLogsResponse)
async def get_compliance_logs(
    limit: int = 100,
    level: str = None,
    category: str = None
):
    """
    Get compliance monitoring logs.
    
    Args:
        limit: Maximum number of logs to return (default: 100)
        level: Filter logs by level (info, warning, error, violation)
        category: Filter logs by category (general, risk, trade, position, leverage)
        
    Returns:
        ComplianceLogsResponse: List of compliance log entries
    """
    try:
        # Get logs from storage
        logs = compliance_logs.copy()
        
        # Apply filters
        if level:
            logs = [log for log in logs if log.level == level]
        if category:
            logs = [log for log in logs if log.category == category]
            
        # Apply limit
        logs = logs[-limit:]
        
        return ComplianceLogsResponse(
            logs=logs,
            count=len(logs)
        )
        
    except Exception as e:
        logger.error(f"Error getting compliance logs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/compliance/check")
async def check_compliance():
    """
    Perform a compliance check on the current trading state.
    This endpoint triggers a comprehensive compliance check across all components.
    
    Returns:
        Dict: Results of the compliance check
    """
    try:
        # Get current risk limits
        risk_limits = signal_router.get_risk_limits()
        
        # Get current positions and performance
        positions = trade_executor.get_positions()
        performance = trade_executor.get_performance_metrics()
        
        # Check drawdown compliance
        current_drawdown = performance.get("drawdown", 0)
        if current_drawdown > risk_limits["maxDrawdown"]:
            add_compliance_log(
                f"Drawdown ({current_drawdown}%) exceeds limit ({risk_limits['maxDrawdown']}%)",
                level="violation",
                category="risk",
                details={
                    "current": current_drawdown,
                    "limit": risk_limits["maxDrawdown"],
                    "difference": current_drawdown - risk_limits["maxDrawdown"]
                }
            )
            
        # Check position size compliance
        for position in positions:
            position_size = position.get("size", 0)
            if position_size > risk_limits["maxPositionSize"]:
                add_compliance_log(
                    f"Position size ({position_size}%) exceeds limit ({risk_limits['maxPositionSize']}%)",
                    level="violation",
                    category="position",
                    details={
                        "symbol": position.get("symbol"),
                        "current": position_size,
                        "limit": risk_limits["maxPositionSize"],
                        "difference": position_size - risk_limits["maxPositionSize"]
                    }
                )
                
        # Check daily trade count
        daily_trades = trade_executor.get_daily_trade_count()
        if daily_trades > risk_limits["maxDailyTrades"]:
            add_compliance_log(
                f"Daily trade count ({daily_trades}) exceeds limit ({risk_limits['maxDailyTrades']})",
                level="violation",
                category="trade",
                details={
                    "current": daily_trades,
                    "limit": risk_limits["maxDailyTrades"],
                    "difference": daily_trades - risk_limits["maxDailyTrades"]
                }
            )
            
        # Add a general compliance check log
        add_compliance_log(
            "Compliance check completed",
            level="info",
            category="general",
            details={
                "timestamp": datetime.now().isoformat(),
                "checks_performed": ["drawdown", "position_size", "daily_trades"]
            }
        )
        
        return {
            "success": True,
            "message": "Compliance check completed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error performing compliance check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add some initial compliance logs
add_compliance_log(
    "Compliance monitoring system initialized",
    level="info",
    category="general"
)
add_compliance_log(
    "Risk limits loaded from configuration",
    level="info",
    category="risk",
    details={"source": "configuration"}
) 