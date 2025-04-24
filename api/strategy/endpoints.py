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

# Available strategies
AVAILABLE_STRATEGIES = [
    "momentum",
    "arbitrage",
    "mean_reversion",
    "sentiment"
]

class StrategyRequest(BaseModel):
    """Request model for setting strategy"""
    strategy: str

class RiskRequest(BaseModel):
    """Request model for setting risk tolerance"""
    risk: int

class StrategyResponse(BaseModel):
    """Response model for strategy endpoints"""
    success: bool
    message: str
    current_strategy: str
    current_risk: int

@router.post("/api/strategy/set", response_model=StrategyResponse)
async def set_strategy(request: StrategyRequest):
    """
    Set the active trading strategy.
    
    Args:
        request: StrategyRequest containing the strategy to set
        
    Returns:
        StrategyResponse: Confirmation of strategy change
    """
    try:
        strategy = request.strategy.lower()
        
        # Validate strategy
        if strategy not in AVAILABLE_STRATEGIES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid strategy. Must be one of: {', '.join(AVAILABLE_STRATEGIES)}"
            )
            
        # Set strategy in signal router
        signal_router.set_strategy(strategy)
        
        # Log the change
        logger.info(f"Strategy changed to: {strategy}")
        
        return StrategyResponse(
            success=True,
            message=f"Strategy set to {strategy}",
            current_strategy=strategy,
            current_risk=signal_router.get_risk_tolerance()
        )
        
    except Exception as e:
        logger.error(f"Error setting strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/api/strategy/risk", response_model=StrategyResponse)
async def set_risk_tolerance(request: RiskRequest):
    """
    Set the risk tolerance level.
    
    Args:
        request: RiskRequest containing the risk level (0-100)
        
    Returns:
        StrategyResponse: Confirmation of risk level change
    """
    try:
        risk = request.risk
        
        # Validate risk level
        if not 0 <= risk <= 100:
            raise HTTPException(
                status_code=400,
                detail="Risk level must be between 0 and 100"
            )
            
        # Set risk tolerance in signal router
        signal_router.set_risk_tolerance(risk)
        
        # Log the change
        logger.info(f"Risk tolerance set to: {risk}%")
        
        return StrategyResponse(
            success=True,
            message=f"Risk tolerance set to {risk}%",
            current_strategy=signal_router.get_current_strategy(),
            current_risk=risk
        )
        
    except Exception as e:
        logger.error(f"Error setting risk tolerance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/api/strategy/current", response_model=StrategyResponse)
async def get_current_strategy():
    """
    Get the current strategy and risk tolerance settings.
    
    Returns:
        StrategyResponse: Current strategy and risk settings
    """
    try:
        return StrategyResponse(
            success=True,
            message="Current strategy settings retrieved",
            current_strategy=signal_router.get_current_strategy(),
            current_risk=signal_router.get_risk_tolerance()
        )
        
    except Exception as e:
        logger.error(f"Error getting current strategy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 