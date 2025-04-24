import sys
import os
from typing import Dict, Any
import numpy as np

# Add the parent directory to the path so we can import the base adapter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_adapter import FibonacciBaseAdapter

class FibonacciRepo2Adapter(FibonacciBaseAdapter):
    """
    Adapter for the second Fibonacci repository.
    This adapter implements an extended Fibonacci retracement calculation
    with additional extensions and projections.
    """
    
    # Standard Fibonacci ratios
    FIB_RATIOS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    # Extension ratios
    EXTENSION_RATIOS = [1.618, 2.618, 3.618, 4.236]
    
    def get_levels(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Fibonacci retracement and extension levels based on price data.
        
        Args:
            price_data: Dictionary containing price information
                Expected keys:
                - 'high': Highest price in the period
                - 'low': Lowest price in the period
                - 'close': Current closing price
                
        Returns:
            Dictionary containing Fibonacci levels
        """
        # Extract price data
        high = price_data.get('high', 0)
        low = price_data.get('low', 0)
        close = price_data.get('close', 0)
        
        # Calculate price range
        price_range = high - low
        
        # Calculate Fibonacci retracement levels
        retracement_levels = {}
        for ratio in self.FIB_RATIOS:
            if ratio == 0:
                retracement_levels[ratio] = low
            elif ratio == 1:
                retracement_levels[ratio] = high
            else:
                retracement_levels[ratio] = high - (price_range * ratio)
        
        # Calculate Fibonacci extension levels
        extension_levels = {}
        for ratio in self.EXTENSION_RATIOS:
            extension_levels[ratio] = high + (price_range * (ratio - 1))
        
        # Determine support and resistance
        support_levels = []
        resistance_levels = []
        
        # Add retracement levels
        for ratio, level in retracement_levels.items():
            if level < close:
                support_levels.append(level)
            else:
                resistance_levels.append(level)
        
        # Add extension levels (always above current price)
        for ratio, level in extension_levels.items():
            resistance_levels.append(level)
        
        # Sort levels
        support_levels.sort(reverse=True)
        resistance_levels.sort()
        
        # Get nearest support and resistance
        nearest_support = support_levels[0] if support_levels else None
        nearest_resistance = resistance_levels[0] if resistance_levels else None
        
        return {
            'support': nearest_support,
            'resistance': nearest_resistance,
            'support_levels': support_levels,
            'resistance_levels': resistance_levels,
            'retracement_levels': retracement_levels,
            'extension_levels': extension_levels
        }
    
    def get_signal(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a trading signal based on Fibonacci analysis.
        
        Args:
            price_data: Dictionary containing price information
            
        Returns:
            Dictionary containing signal information
        """
        # Get Fibonacci levels
        levels = self.get_levels(price_data)
        
        # Extract data
        close = price_data.get('close', 0)
        nearest_support = levels.get('support')
        nearest_resistance = levels.get('resistance')
        
        # Initialize signal
        signal = {
            'action': 'HOLD',
            'confidence': 0.0
        }
        
        # Calculate distance to nearest levels
        if nearest_support and nearest_resistance:
            support_distance = (close - nearest_support) / close
            resistance_distance = (nearest_resistance - close) / close
            
            # Generate signal based on proximity to levels
            # This implementation uses a more conservative approach
            if support_distance < 0.005:  # Within 0.5% of support
                signal['action'] = 'BUY'
                signal['confidence'] = 0.8
            elif resistance_distance < 0.005:  # Within 0.5% of resistance
                signal['action'] = 'SELL'
                signal['confidence'] = 0.8
            elif support_distance < 0.01:  # Within 1% of support
                signal['action'] = 'BUY'
                signal['confidence'] = 0.6
            elif resistance_distance < 0.01:  # Within 1% of resistance
                signal['action'] = 'SELL'
                signal['confidence'] = 0.6
        
        return signal 