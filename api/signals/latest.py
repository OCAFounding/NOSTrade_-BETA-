from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
import logging
import time
from pydantic import BaseModel
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

class Alert(BaseModel):
    """Alert model"""
    title: str
    description: str
    time: str
    severity: str = "info"  # info, warning, error

class Signal(BaseModel):
    """Signal model"""
    source: str
    action: str
    reason: str
    confidence: float

class ConfidenceData(BaseModel):
    """Confidence data model"""
    name: str
    confidence: float

class SignalResponse(BaseModel):
    """Response model for the signals endpoint"""
    signals: List[Signal]
    confidences: List[ConfidenceData]
    alerts: List[Alert]
    timestamp: float

@router.get("/api/signals/latest", response_model=SignalResponse)
async def get_latest_signals():
    """
    Get the latest signals from the trading system.
    
    Returns:
        SignalResponse: The latest signals, confidence data, and alerts
    """
    try:
        # Get market data
        market_data = signal_router._get_market_data()
        
        # Get signals from the adapter system
        adapter_signal = signal_router.fibonacci_factory.get_signal(market_data)
        
        # Get signals from the fibonacci ensemble
        ensemble_signal = signal_router._get_ensemble_signal()
        
        # Combine signals
        combined_signal = signal_router._combine_signals(adapter_signal, ensemble_signal)
        
        # Analyze with parent AI
        action = parent_ai.analyze_signal(combined_signal)
        
        # Format signals for response
        signals = [
            Signal(
                source="Fibonacci Adapter",
                action=adapter_signal["action"],
                reason="Based on Fibonacci retracement levels",
                confidence=adapter_signal["confidence"]
            ),
            Signal(
                source="Fibonacci Ensemble",
                action=ensemble_signal,
                reason="Combined analysis of multiple Fibonacci strategies",
                confidence=0.8  # Example confidence
            )
        ]
        
        # Get current position
        position = trade_executor.get_position()
        
        # Add position to signals
        signals.append(
            Signal(
                source="Current Position",
                action=f"{position['position']} {position['symbol']}",
                reason="Current trading position",
                confidence=1.0
            )
        )
        
        # Format confidence data for the chart
        confidences = [
            ConfidenceData(name="Fibonacci Adapter", confidence=adapter_signal["confidence"] * 100),
            ConfidenceData(name="Fibonacci Ensemble", confidence=0.8 * 100),  # Example confidence
            ConfidenceData(name="Position", confidence=100.0)
        ]
        
        # Generate alerts based on signal analysis
        alerts = []
        
        # Check for high confidence signals
        if combined_signal["confidence"] > 0.8:
            alerts.append(
                Alert(
                    title="High Confidence Signal",
                    description=f"Strong {action} signal detected with {combined_signal['confidence']:.2%} confidence",
                    time=datetime.now().isoformat(),
                    severity="info"
                )
            )
            
        # Check for position changes
        if abs(position["position"]) > 0:
            alerts.append(
                Alert(
                    title="Active Position",
                    description=f"Currently holding {position['position']} {position['symbol']}",
                    time=datetime.now().isoformat(),
                    severity="info"
                )
            )
            
        # Check for potential risks
        if combined_signal["confidence"] < 0.3:
            alerts.append(
                Alert(
                    title="Low Confidence Warning",
                    description="Signal confidence below 30%. Consider holding current position.",
                    time=datetime.now().isoformat(),
                    severity="warning"
                )
            )
            
        # Return response
        return SignalResponse(
            signals=signals,
            confidences=confidences,
            alerts=alerts,
            timestamp=time.time()
        )
        
    except Exception as e:
        logger.error(f"Error getting latest signals: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 