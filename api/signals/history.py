from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
from pydantic import BaseModel
from datetime import datetime, timedelta

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

class HistoricalSignal(BaseModel):
    """Historical signal model"""
    timestamp: float
    action: str
    confidence: float
    source: str

class HistoricalResponse(BaseModel):
    """Response model for historical signals"""
    signals: List[HistoricalSignal]
    start_time: float
    end_time: float

@router.get("/api/signals/history", response_model=HistoricalResponse)
async def get_historical_signals(
    hours: int = 24,
    source: str = None
):
    """
    Get historical signals from the trading system.
    
    Args:
        hours: Number of hours of history to retrieve (default: 24)
        source: Optional source to filter signals by
        
    Returns:
        HistoricalResponse: Historical signals within the specified time range
    """
    try:
        # Calculate time range
        end_time = datetime.now().timestamp()
        start_time = end_time - (hours * 3600)
        
        # Get signal history from parent AI
        signal_history = parent_ai.get_signal_history()
        
        # Get trade history
        trade_history = trade_executor.get_trade_history()
        
        # Combine and format historical signals
        historical_signals = []
        
        # Add AI signals
        for signal in signal_history:
            if signal.get("timestamp", 0) >= start_time:
                historical_signals.append(
                    HistoricalSignal(
                        timestamp=signal["timestamp"],
                        action=signal.get("action", "HOLD"),
                        confidence=signal.get("confidence", 0.0),
                        source="AI Analysis"
                    )
                )
                
        # Add trade signals
        for trade in trade_history:
            if trade.get("timestamp", 0) >= start_time:
                historical_signals.append(
                    HistoricalSignal(
                        timestamp=trade["timestamp"],
                        action=trade["action"],
                        confidence=1.0,  # Trades are executed with full confidence
                        source="Trade Execution"
                    )
                )
                
        # Sort by timestamp
        historical_signals.sort(key=lambda x: x.timestamp)
        
        # Filter by source if specified
        if source:
            historical_signals = [
                signal for signal in historical_signals
                if signal.source.lower() == source.lower()
            ]
            
        return HistoricalResponse(
            signals=historical_signals,
            start_time=start_time,
            end_time=end_time
        )
        
    except Exception as e:
        logger.error(f"Error getting historical signals: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 