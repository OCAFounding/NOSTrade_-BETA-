from typing import Dict, List, Any, Tuple
import numpy as np
from .base_adapter import BaseFibonacciAdapter

class EnsembleFibonacciAdapter(BaseFibonacciAdapter):
    """
    Ensemble Fibonacci adapter that combines multiple Fibonacci strategies
    from various sources to improve accuracy and robustness.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the ensemble Fibonacci adapter.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        super().__init__(config)
        self.strategies = [
            self._strategy_harshgupta,
            self._strategy_brandon,
            self._strategy_ranjit,
            self._strategy_joengelh,
            self._strategy_faraway,
            self._strategy_nerr,
            self._strategy_doombringer
        ]
        
    def get_levels(self, market_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        Calculate Fibonacci levels based on market data using ensemble approach.
        
        Args:
            market_data: Dictionary containing market data (OHLCV, etc.)
            
        Returns:
            Dictionary with 'support' and 'resistance' keys, each containing a list of price levels
        """
        if not self._validate_market_data(market_data):
            self.logger.error("Invalid market data provided")
            return {'support': [], 'resistance': []}
            
        # Extract price data
        closes = market_data['close']
        highs = market_data['high']
        lows = market_data['low']
        
        # Collect support and resistance levels from all strategies
        support_levels = []
        resistance_levels = []
        
        for strategy in self.strategies:
            result = strategy(market_data)
            support_levels.append(result['support'])
            resistance_levels.append(result['resistance'])
            
        # Calculate ensemble averages
        ensemble_support = np.mean(support_levels)
        ensemble_resistance = np.mean(resistance_levels)
        
        # Return both the ensemble averages and individual levels
        return {
            'support': [ensemble_support],
            'resistance': [ensemble_resistance],
            'support_levels': support_levels,
            'resistance_levels': resistance_levels,
            'strategies_used': len(self.strategies)
        }
        
    def get_signal(self, market_data: Dict[str, Any], current_price: float) -> Tuple[str, float]:
        """
        Generate a trading signal based on market data and current price.
        
        Args:
            market_data: Dictionary containing market data (OHLCV, etc.)
            current_price: Current market price
            
        Returns:
            Tuple containing (signal_type, confidence)
            signal_type: 'buy', 'sell', or 'hold'
            confidence: Float between 0 and 1 indicating signal confidence
        """
        if not self._validate_market_data(market_data):
            self.logger.error("Invalid market data provided")
            return 'hold', 0.0
            
        # Get Fibonacci levels
        levels = self.get_levels(market_data)
        if not levels['support'] or not levels['resistance']:
            return 'hold', 0.0
            
        # Get ensemble support and resistance
        ensemble_support = levels['support'][0]
        ensemble_resistance = levels['resistance'][0]
        
        # Calculate confidence based on proximity to levels
        support_distance = current_price - ensemble_support
        resistance_distance = ensemble_resistance - current_price
        total_range = resistance_distance + support_distance
        
        # Determine signal based on price position relative to Fibonacci levels
        if total_range == 0:
            return 'hold', 0.0
            
        # Calculate confidence based on proximity to levels
        if support_distance < resistance_distance:
            confidence = 1 - (support_distance / total_range)
            return 'buy', confidence
        else:
            confidence = 1 - (resistance_distance / total_range)
            return 'sell', confidence
            
    # === Individual Strategy Implementations ===
    
    def _strategy_harshgupta(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from harshgupta repository."""
        high = max(data["high"])
        low = min(data["low"])
        diff = high - low
        return {
            "support": low + diff * 0.236,
            "resistance": high - diff * 0.236
        }
        
    def _strategy_brandon(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from brandon repository."""
        high = max(data["high"])
        low = min(data["low"])
        return {
            "support": low + (high - low) * 0.382,
            "resistance": high - (high - low) * 0.382
        }
        
    def _strategy_ranjit(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from ranjit repository."""
        close = np.array(data["close"])
        peak = np.max(close)
        trough = np.min(close)
        diff = peak - trough
        return {
            "support": trough + 0.5 * diff,
            "resistance": peak - 0.5 * diff
        }
        
    def _strategy_joengelh(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from joengelh repository."""
        high = max(data["high"])
        low = min(data["low"])
        return {
            "support": low + (high - low) * 0.618,
            "resistance": high - (high - low) * 0.618
        }
        
    def _strategy_faraway(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from faraway repository."""
        high = np.mean(data["high"][-20:])
        low = np.mean(data["low"][-20:])
        return {
            "support": low + 0.382 * (high - low),
            "resistance": high - 0.382 * (high - low)
        }
        
    def _strategy_nerr(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from nerr repository."""
        close = np.array(data["close"])
        sma = np.mean(close[-10:])
        return {
            "support": sma * 0.95,
            "resistance": sma * 1.05
        }
        
    def _strategy_doombringer(self, data: Dict[str, List[float]]) -> Dict[str, float]:
        """Strategy from doombringer repository."""
        low = min(data["low"])
        high = max(data["high"])
        return {
            "support": low + (high - low) * 0.786,
            "resistance": high - (high - low) * 0.786
        } 