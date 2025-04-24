import sys
import os
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Add the parent directory to the path so we can import the base adapter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_adapter import FibonacciBaseAdapter

class FibonacciRepo3Adapter(FibonacciBaseAdapter):
    """
    Adapter for the third Fibonacci repository.
    This adapter implements a machine learning approach to Fibonacci analysis.
    """
    
    # Standard Fibonacci ratios
    FIB_RATIOS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    def __init__(self):
        """Initialize the ML model and scaler."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _extract_features(self, price_data: Dict[str, Any], fib_levels: Dict[float, float]) -> np.ndarray:
        """
        Extract features from price data and Fibonacci levels.
        
        Args:
            price_data: Dictionary containing price information
            fib_levels: Dictionary of Fibonacci levels
            
        Returns:
            NumPy array of features
        """
        # Extract price data
        close = price_data.get('close', 0)
        
        # Initialize features list
        features = []
        
        # Add Fibonacci level features
        for ratio, level in fib_levels.items():
            # Distance to each Fibonacci level
            distance = (close - level) / close
            features.append(distance)
        
        # Add price momentum (if available)
        if 'returns' in price_data:
            features.append(price_data['returns'])
        
        # Add volatility (if available)
        if 'volatility' in price_data:
            features.append(price_data['volatility'])
        
        # Add volume features (if available)
        if 'volume_ratio' in price_data:
            features.append(price_data['volume_ratio'])
        
        # Return as numpy array
        return np.array(features).reshape(1, -1)
    
    def _predict_price_movement(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Predict price movement using the ML model.
        
        Args:
            features: NumPy array of features
            
        Returns:
            Tuple of (predicted_action, confidence)
        """
        if not self.is_trained:
            # If model is not trained, return default values
            return 'HOLD', 0.0
        
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(scaled_features)[0]
        
        # Get predicted class
        predicted_class = self.model.predict(scaled_features)[0]
        
        # Map class to action
        action_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
        action = action_map.get(predicted_class, 'HOLD')
        
        # Calculate confidence
        confidence = probabilities[predicted_class]
        
        return action, confidence
    
    def get_levels(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Fibonacci retracement levels based on price data.
        
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
        
        # Calculate Fibonacci levels
        retracement_levels = {}
        for ratio in self.FIB_RATIOS:
            if ratio == 0:
                retracement_levels[ratio] = low
            elif ratio == 1:
                retracement_levels[ratio] = high
            else:
                retracement_levels[ratio] = high - (price_range * ratio)
        
        # Determine support and resistance
        support_levels = []
        resistance_levels = []
        
        for ratio, level in retracement_levels.items():
            if level < close:
                support_levels.append(level)
            else:
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
            'retracement_levels': retracement_levels
        }
    
    def get_signal(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a trading signal based on Fibonacci analysis and ML prediction.
        
        Args:
            price_data: Dictionary containing price information
            
        Returns:
            Dictionary containing signal information
        """
        # Get Fibonacci levels
        levels = self.get_levels(price_data)
        
        # Extract features for ML prediction
        features = self._extract_features(price_data, levels['retracement_levels'])
        
        # Predict price movement
        ml_action, ml_confidence = self._predict_price_movement(features)
        
        # If ML model is not trained or confidence is low, use traditional approach
        if not self.is_trained or ml_confidence < 0.6:
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
                if support_distance < 0.01:  # Within 1% of support
                    signal['action'] = 'BUY'
                    signal['confidence'] = 0.7
                elif resistance_distance < 0.01:  # Within 1% of resistance
                    signal['action'] = 'SELL'
                    signal['confidence'] = 0.7
        else:
            # Use ML prediction
            signal = {
                'action': ml_action,
                'confidence': ml_confidence
            }
        
        return signal 