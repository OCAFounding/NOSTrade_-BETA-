from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
import logging

class BaseFibonacciAdapter(ABC):
    """
    Base class for all Fibonacci adapters.
    All specific adapters should inherit from this class and implement the abstract methods.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Dictionary containing adapter-specific configuration
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def get_levels(self, market_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """
        Calculate Fibonacci levels based on market data.
        
        Args:
            market_data: Dictionary containing market data (OHLCV, etc.)
            
        Returns:
            Dictionary with 'support' and 'resistance' keys, each containing a list of price levels
        """
        pass
    
    @abstractmethod
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
        pass
    
    def _validate_market_data(self, market_data: Dict[str, Any]) -> bool:
        """
        Validate that the market data contains all required fields.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Boolean indicating if the market data is valid
        """
        required_fields = ['open', 'high', 'low', 'close', 'volume']
        return all(field in market_data for field in required_fields)
    
    def _find_swing_points(self, prices: List[float], min_points: int = 5) -> Tuple[List[int], List[int]]:
        """
        Find swing highs and lows in a price series.
        
        Args:
            prices: List of price values
            min_points: Minimum number of points to consider for swing detection
            
        Returns:
            Tuple containing lists of indices for swing highs and lows
        """
        if len(prices) < min_points:
            self.logger.warning(f"Not enough price points for swing detection. Need at least {min_points}.")
            return [], []
            
        swing_highs = []
        swing_lows = []
        
        for i in range(2, len(prices) - 2):
            # Check for swing high
            if prices[i] > prices[i-1] and prices[i] > prices[i-2] and \
               prices[i] > prices[i+1] and prices[i] > prices[i+2]:
                swing_highs.append(i)
                
            # Check for swing low
            if prices[i] < prices[i-1] and prices[i] < prices[i-2] and \
               prices[i] < prices[i+1] and prices[i] < prices[i+2]:
                swing_lows.append(i)
                
        return swing_highs, swing_lows
    
    def _calculate_fibonacci_levels(self, start_price: float, end_price: float) -> Dict[str, List[float]]:
        """
        Calculate Fibonacci retracement and extension levels.
        
        Args:
            start_price: Starting price for the Fibonacci calculation
            end_price: Ending price for the Fibonacci calculation
            
        Returns:
            Dictionary with 'support' and 'resistance' keys, each containing a list of price levels
        """
        price_range = end_price - start_price
        
        # Get Fibonacci ratios from config or use defaults
        fib_ratios = self.config.get('fibonacci_levels', [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1])
        
        # Calculate retracement levels
        retracement_levels = [start_price + (price_range * ratio) for ratio in fib_ratios]
        
        # Calculate extension levels if enabled
        extension_levels = []
        if self.config.get('use_extension_levels', False):
            ext_ratios = self.config.get('extension_levels', [1.618, 2.618, 3.618])
            extension_levels = [start_price + (price_range * ratio) for ratio in ext_ratios]
        
        # Determine support and resistance based on price direction
        if end_price > start_price:
            support = retracement_levels
            resistance = extension_levels
        else:
            support = extension_levels
            resistance = retracement_levels
            
        return {
            'support': support,
            'resistance': resistance
        } 