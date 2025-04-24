import logging
from typing import Dict, Any, List, Optional
import numpy as np

class ParentAI:
    """
    Parent AI agent that analyzes signals from various sources and makes trading decisions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Parent AI agent.
        
        Args:
            config: Optional configuration dictionary
        """
        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load configuration
        self.config = config or {}
        self.confidence_threshold = self.config.get('confidence_threshold', 0.6)
        self.signal_history = []
        self.max_history_size = self.config.get('max_signal_history', 100)
        
        self.logger.info("Parent AI agent initialized")
        
    def analyze_signal(self, signal: Dict[str, Any]) -> str:
        """
        Analyze the signal and make a trading decision.
        
        Args:
            signal: Dictionary containing signal information
            
        Returns:
            Trading decision: "BUY", "SELL", or "HOLD"
        """
        try:
            # Add signal to history
            self._add_to_history(signal)
            
            # Extract signal components
            action = signal.get('action', 'hold')
            confidence = signal.get('confidence', 0.0)
            
            # Check if confidence meets threshold
            if confidence < self.confidence_threshold:
                self.logger.info(f"Signal confidence {confidence:.2f} below threshold {self.confidence_threshold}")
                return "HOLD"
                
            # Apply additional analysis based on signal history
            decision = self._apply_historical_analysis(action, confidence)
            
            # Log decision
            self.logger.info(f"Decision: {decision}, Action: {action}, Confidence: {confidence:.2f}")
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Error analyzing signal: {str(e)}")
            return "HOLD"
            
    def _add_to_history(self, signal: Dict[str, Any]):
        """
        Add signal to history, maintaining the maximum history size.
        
        Args:
            signal: Signal to add to history
        """
        self.signal_history.append(signal)
        
        # Trim history if it exceeds the maximum size
        if len(self.signal_history) > self.max_history_size:
            self.signal_history = self.signal_history[-self.max_history_size:]
            
    def _apply_historical_analysis(self, action: str, confidence: float) -> str:
        """
        Apply historical analysis to the signal.
        
        Args:
            action: Current signal action
            confidence: Current signal confidence
            
        Returns:
            Trading decision: "BUY", "SELL", or "HOLD"
        """
        # If history is too short, just use the current signal
        if len(self.signal_history) < 3:
            return action.upper()
            
        # Get recent signals
        recent_signals = self.signal_history[-3:]
        
        # Count occurrences of each action
        action_counts = {'buy': 0, 'sell': 0, 'hold': 0}
        for signal in recent_signals:
            action_counts[signal.get('action', 'hold')] += 1
            
        # Check for trend consistency
        if action_counts[action] >= 2:
            # Trend is consistent, use the current action
            return action.upper()
            
        # Check for conflicting signals
        if action_counts['buy'] > 0 and action_counts['sell'] > 0:
            # Conflicting signals, be conservative
            return "HOLD"
            
        # If we get here, use the current action
        return action.upper()
        
    def get_signal_history(self) -> List[Dict[str, Any]]:
        """
        Get the signal history.
        
        Returns:
            List of historical signals
        """
        return self.signal_history.copy()
        
    def reset_history(self):
        """Reset the signal history."""
        self.signal_history = []
        self.logger.info("Signal history reset") 