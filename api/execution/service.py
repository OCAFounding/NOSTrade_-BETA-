from typing import Dict, Any, List, Optional
import logging
import uuid
from datetime import datetime, timedelta
from .config import get_execution_config

class ExecutionService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = get_execution_config()
        self.final_signals = []
        self.execution_status = []
        self.max_status_entries = 100  # Keep last 100 status entries
        
    def get_final_decisions(self) -> Dict[str, Any]:
        """
        Get the current final decisions and execution status.
        
        Returns:
            Dict containing final signals and execution status
        """
        self.logger.info("Getting final decisions")
        
        # Update final signals if needed
        if self._should_update_signals():
            self._update_final_signals()
            
        # Clean up old status entries
        self._cleanup_status_entries()
        
        return {
            "signals": self.final_signals,
            "status": self.execution_status
        }
    
    def execute_signal(self, signal_id: str) -> Dict[str, Any]:
        """
        Execute a trade signal.
        
        Args:
            signal_id: ID of the signal to execute
            
        Returns:
            Dict containing execution result
        """
        self.logger.info(f"Executing signal {signal_id}")
        
        # Find the signal
        signal = next((s for s in self.final_signals if s["id"] == signal_id), None)
        if not signal:
            raise ValueError(f"Signal {signal_id} not found")
            
        # Check if signal is still valid
        if not self._is_signal_valid(signal):
            raise ValueError(f"Signal {signal_id} is no longer valid")
            
        # Execute the trade
        try:
            # In a real implementation, this would call the trading API
            execution_result = self._execute_trade(signal)
            
            # Add to execution status
            status_entry = {
                "id": str(uuid.uuid4()),
                "signal_id": signal_id,
                "asset": signal["asset"],
                "action": signal["action"],
                "message": "Trade executed successfully",
                "timestamp": datetime.now().isoformat(),
                "details": execution_result
            }
            self.execution_status.append(status_entry)
            
            # Remove the executed signal
            self.final_signals = [s for s in self.final_signals if s["id"] != signal_id]
            
            return {
                "success": True,
                "message": "Trade executed successfully",
                "execution_id": status_entry["id"]
            }
            
        except Exception as e:
            self.logger.error(f"Error executing trade: {str(e)}")
            
            # Add failed execution to status
            status_entry = {
                "id": str(uuid.uuid4()),
                "signal_id": signal_id,
                "asset": signal["asset"],
                "action": signal["action"],
                "message": f"Trade execution failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            self.execution_status.append(status_entry)
            
            raise
    
    def _should_update_signals(self) -> bool:
        """Check if signals need to be updated based on config settings."""
        if not self.final_signals:
            return True
            
        # Check if any signals are expired
        return any(not self._is_signal_valid(signal) for signal in self.final_signals)
    
    def _update_final_signals(self) -> None:
        """Update the final signals list."""
        self.logger.info("Updating final signals")
        
        # In a real implementation, this would fetch from the decision engine
        # For demonstration, we'll generate some sample signals
        self.final_signals = [
            {
                "id": str(uuid.uuid4()),
                "asset": "BTC",
                "action": "BUY",
                "confidence": 85,
                "timestamp": datetime.now().isoformat(),
                "expiry": (datetime.now() + timedelta(minutes=30)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "asset": "ETH",
                "action": "SELL",
                "confidence": 78,
                "timestamp": datetime.now().isoformat(),
                "expiry": (datetime.now() + timedelta(minutes=30)).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "asset": "SOL",
                "action": "BUY",
                "confidence": 92,
                "timestamp": datetime.now().isoformat(),
                "expiry": (datetime.now() + timedelta(minutes=30)).isoformat()
            }
        ]
        
        self.logger.info(f"Updated final signals: {len(self.final_signals)} signals")
    
    def _is_signal_valid(self, signal: Dict[str, Any]) -> bool:
        """Check if a signal is still valid."""
        expiry = datetime.fromisoformat(signal["expiry"])
        return datetime.now() < expiry
    
    def _execute_trade(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a trade based on a signal."""
        # In a real implementation, this would call the trading API
        # For demonstration, we'll simulate a successful trade
        return {
            "price": 50000.0,
            "amount": 0.1,
            "total": 5000.0,
            "fee": 5.0,
            "execution_time": datetime.now().isoformat()
        }
    
    def _cleanup_status_entries(self) -> None:
        """Clean up old status entries."""
        if len(self.execution_status) > self.max_status_entries:
            self.execution_status = self.execution_status[-self.max_status_entries:] 