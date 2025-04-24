import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

class FibonacciStrategy:
    """
    Fibonacci retracement strategy for technical analysis.
    This strategy calculates Fibonacci retracement levels and identifies potential
    support and resistance levels based on price action.
    """
    
    # Standard Fibonacci ratios
    FIB_RATIOS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    def __init__(self, lookback_period: int = 100):
        """
        Initialize the Fibonacci strategy.
        
        Args:
            lookback_period: Number of candles to look back for swing highs/lows
        """
        self.lookback_period = lookback_period
    
    def calculate_fib_levels(self, high: float, low: float) -> Dict[float, float]:
        """
        Calculate Fibonacci retracement levels between a high and low price.
        
        Args:
            high: The swing high price
            low: The swing low price
            
        Returns:
            Dictionary mapping Fibonacci ratios to price levels
        """
        price_range = high - low
        levels = {}
        
        for ratio in self.FIB_RATIOS:
            if ratio == 0:
                levels[ratio] = low
            elif ratio == 1:
                levels[ratio] = high
            else:
                levels[ratio] = high - (price_range * ratio)
                
        return levels
    
    def find_swing_points(self, df: pd.DataFrame) -> Tuple[float, float]:
        """
        Find swing high and low points in the price data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Tuple of (swing_high, swing_low)
        """
        # Simple implementation - can be enhanced with more sophisticated algorithms
        high = df['high'].max()
        low = df['low'].min()
        return high, low
    
    def identify_support_resistance(self, current_price: float, fib_levels: Dict[float, float]) -> Dict[str, List[float]]:
        """
        Identify potential support and resistance levels based on Fibonacci retracement.
        
        Args:
            current_price: Current market price
            fib_levels: Dictionary of Fibonacci levels
            
        Returns:
            Dictionary with 'support' and 'resistance' lists
        """
        support_levels = []
        resistance_levels = []
        
        for ratio, level in fib_levels.items():
            if level < current_price:
                support_levels.append(level)
            else:
                resistance_levels.append(level)
                
        return {
            'support': sorted(support_levels, reverse=True),
            'resistance': sorted(resistance_levels)
        }
    
    def generate_signal(self, df: pd.DataFrame, current_price: float) -> Dict:
        """
        Generate trading signal based on Fibonacci retracement analysis.
        
        Args:
            df: DataFrame with OHLCV data
            current_price: Current market price
            
        Returns:
            Dictionary with signal information
        """
        # Find swing points
        swing_high, swing_low = self.find_swing_points(df)
        
        # Calculate Fibonacci levels
        fib_levels = self.calculate_fib_levels(swing_high, swing_low)
        
        # Identify support and resistance
        levels = self.identify_support_resistance(current_price, fib_levels)
        
        # Determine signal
        nearest_support = levels['support'][0] if levels['support'] else None
        nearest_resistance = levels['resistance'][0] if levels['resistance'] else None
        
        # Calculate distance to nearest levels
        support_distance = (current_price - nearest_support) / current_price if nearest_support else float('inf')
        resistance_distance = (nearest_resistance - current_price) / current_price if nearest_resistance else float('inf')
        
        # Generate signal
        signal = {
            'action': 'HOLD',
            'confidence': 0.0,
            'support_levels': levels['support'],
            'resistance_levels': levels['resistance'],
            'nearest_support': nearest_support,
            'nearest_resistance': nearest_resistance,
            'fib_levels': fib_levels
        }
        
        # Simple signal logic - can be enhanced
        if support_distance < 0.01:  # Within 1% of support
            signal['action'] = 'BUY'
            signal['confidence'] = 0.7
        elif resistance_distance < 0.01:  # Within 1% of resistance
            signal['action'] = 'SELL'
            signal['confidence'] = 0.7
            
        return signal 