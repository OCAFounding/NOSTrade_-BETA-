from typing import Dict, List, Any, Tuple
import numpy as np
from .base_adapter import BaseFibonacciAdapter

class BasicFibonacciAdapter(BaseFibonacciAdapter):
    """
    Basic Fibonacci adapter implementation that uses traditional retracement levels
    and swing points to identify support and resistance levels.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the basic Fibonacci adapter.
        
        Args:
            config: Dictionary containing adapter configuration
        """
        super().__init__(config)
        self.min_swing_points = config.get('min_swing_points', 5)
        self.trend_confirmation_period = config.get('trend_confirmation_period', 14)
        
    def get_levels(self, market_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        Calculate Fibonacci levels based on market data.
        
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
        
        # Find swing points
        swing_highs, swing_lows = self._find_swing_points(closes, self.min_swing_points)
        
        if not swing_highs or not swing_lows:
            self.logger.warning("Not enough swing points found for Fibonacci calculation")
            return {'support': [], 'resistance': []}
            
        # Determine trend direction using simple moving average
        sma = np.mean(closes[-self.trend_confirmation_period:])
        current_price = closes[-1]
        trend_direction = 'up' if current_price > sma else 'down'
        
        # Calculate Fibonacci levels based on most recent swing points
        if trend_direction == 'up':
            start_price = lows[swing_lows[-1]]
            end_price = highs[swing_highs[-1]]
        else:
            start_price = highs[swing_highs[-1]]
            end_price = lows[swing_lows[-1]]
            
        return self._calculate_fibonacci_levels(start_price, end_price)
        
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
            
        # Calculate confidence based on proximity to Fibonacci levels
        support_levels = sorted(levels['support'])
        resistance_levels = sorted(levels['resistance'])
        
        # Find nearest support and resistance levels
        nearest_support = max([level for level in support_levels if level < current_price], default=min(support_levels))
        nearest_resistance = min([level for level in resistance_levels if level > current_price], default=max(resistance_levels))
        
        # Calculate price ranges
        support_range = current_price - nearest_support
        resistance_range = nearest_resistance - current_price
        total_range = resistance_range + support_range
        
        # Determine signal based on price position relative to Fibonacci levels
        if total_range == 0:
            return 'hold', 0.0
            
        # Calculate confidence based on proximity to levels
        if support_range < resistance_range:
            confidence = 1 - (support_range / total_range)
            return 'buy', confidence
        else:
            confidence = 1 - (resistance_range / total_range)
            return 'sell', confidence 