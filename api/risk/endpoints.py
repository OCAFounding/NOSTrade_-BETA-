from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
from pydantic import BaseModel

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

# Default risk limits
DEFAULT_RISK_LIMITS = {
    "maxDrawdown": 5,  # 5% maximum drawdown
    "stopLoss": 2,     # 2% stop-loss threshold
    "maxPositionSize": 10,  # 10% maximum position size
    "maxLeverage": 1,  # No leverage by default
    "maxDailyTrades": 20  # Maximum number of trades per day
}

# Current risk limits (in-memory storage)
current_risk_limits = DEFAULT_RISK_LIMITS.copy()

class RiskLimitsRequest(BaseModel):
    """Request model for updating risk limits"""
    maxDrawdown: float = None
    stopLoss: float = None
    maxPositionSize: float = None
    maxLeverage: float = None
    maxDailyTrades: int = None

class RiskLimitsResponse(BaseModel):
    """Response model for risk limits endpoints"""
    success: bool
    message: str
    limits: Dict[str, float]

@router.post("/api/risk/update", response_model=RiskLimitsResponse)
async def update_risk_limits(request: RiskLimitsRequest):
    """
    Update risk management parameters.
    
    Args:
        request: RiskLimitsRequest containing the risk limits to update
        
    Returns:
        RiskLimitsResponse: Confirmation of risk limits update
    """
    try:
        global current_risk_limits
        
        # Update only the provided limits
        if request.maxDrawdown is not None:
            if not 0 < request.maxDrawdown <= 100:
                raise HTTPException(
                    status_code=400,
                    detail="Max drawdown must be between 0 and 100"
                )
            current_risk_limits["maxDrawdown"] = request.maxDrawdown
            
        if request.stopLoss is not None:
            if not 0 < request.stopLoss <= 100:
                raise HTTPException(
                    status_code=400,
                    detail="Stop-loss must be between 0 and 100"
                )
            current_risk_limits["stopLoss"] = request.stopLoss
            
        if request.maxPositionSize is not None:
            if not 0 < request.maxPositionSize <= 100:
                raise HTTPException(
                    status_code=400,
                    detail="Max position size must be between 0 and 100"
                )
            current_risk_limits["maxPositionSize"] = request.maxPositionSize
            
        if request.maxLeverage is not None:
            if not 0 <= request.maxLeverage <= 10:
                raise HTTPException(
                    status_code=400,
                    detail="Max leverage must be between 0 and 10"
                )
            current_risk_limits["maxLeverage"] = request.maxLeverage
            
        if request.maxDailyTrades is not None:
            if not 0 < request.maxDailyTrades <= 100:
                raise HTTPException(
                    status_code=400,
                    detail="Max daily trades must be between 0 and 100"
                )
            current_risk_limits["maxDailyTrades"] = request.maxDailyTrades
            
        # Apply risk limits to trading components
        signal_router.set_risk_limits(current_risk_limits)
        trade_executor.set_risk_limits(current_risk_limits)
        
        # Log the change
        logger.info(f"Risk limits updated: {current_risk_limits}")
        
        return RiskLimitsResponse(
            success=True,
            message="Risk limits updated successfully",
            limits=current_risk_limits
        )
        
    except Exception as e:
        logger.error(f"Error updating risk limits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/api/risk/current", response_model=RiskLimitsResponse)
async def get_current_risk_limits():
    """
    Get the current risk management parameters.
    
    Returns:
        RiskLimitsResponse: Current risk limits
    """
    try:
        return RiskLimitsResponse(
            success=True,
            message="Current risk limits retrieved",
            limits=current_risk_limits
        )
        
    except Exception as e:
        logger.error(f"Error getting current risk limits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/api/risk/reset", response_model=RiskLimitsResponse)
async def reset_risk_limits():
    """
    Reset risk management parameters to default values.
    
    Returns:
        RiskLimitsResponse: Confirmation of risk limits reset
    """
    try:
        global current_risk_limits
        current_risk_limits = DEFAULT_RISK_LIMITS.copy()
        
        # Apply default risk limits to trading components
        signal_router.set_risk_limits(current_risk_limits)
        trade_executor.set_risk_limits(current_risk_limits)
        
        # Log the change
        logger.info("Risk limits reset to default values")
        
        return RiskLimitsResponse(
            success=True,
            message="Risk limits reset to default values",
            limits=current_risk_limits
        )
        
    except Exception as e:
        logger.error(f"Error resetting risk limits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 