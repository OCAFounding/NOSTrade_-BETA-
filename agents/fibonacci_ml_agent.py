from agents.child_agent import ChildAgent
from strategies.fibonacci_strategy import FibonacciStrategy
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class FibonacciMLAgent(ChildAgent):
    """
    Child agent that specializes in Fibonacci retracement analysis with ML prediction.
    This agent uses Fibonacci retracement levels and machine learning to predict
    price movements and generate trading signals.
    """
    
    def __init__(self, name: str = "FibonacciMLAgent", lookback_period: int = 100, model_path: str = None):
        """
        Initialize the Fibonacci ML agent.
        
        Args:
            name: Name of the agent
            lookback_period: Number of candles to look back for swing highs/lows
            model_path: Path to the saved ML model (if None, a new model will be created)
        """
        # Create the base Fibonacci strategy
        strategy = FibonacciStrategy(lookback_period=lookback_period)
        
        # Initialize the child agent with the strategy function
        super().__init__(name, self._execute_strategy)
        
        # Store the strategy instance
        self.strategy = strategy
        
        # Initialize ML components
        self.model = None
        self.scaler = StandardScaler()
        
        # Load or create the ML model
        if model_path and os.path.exists(model_path):
            self._load_model(model_path)
        else:
            self._create_model()
    
    def _create_model(self):
        """Create a new ML model for Fibonacci prediction."""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    
    def _load_model(self, model_path: str):
        """Load a saved ML model."""
        try:
            model_data = joblib.load(model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
        except Exception as e:
            print(f"Error loading model: {e}")
            self._create_model()
    
    def _save_model(self, model_path: str):
        """Save the ML model."""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler
            }
            joblib.dump(model_data, model_path)
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def _extract_features(self, df: pd.DataFrame, fib_levels: Dict[float, float]) -> np.ndarray:
        """
        Extract features from the price data and Fibonacci levels.
        
        Args:
            df: DataFrame with OHLCV data
            fib_levels: Dictionary of Fibonacci levels
            
        Returns:
            NumPy array of features
        """
        # Basic price features
        features = []
        
        # Price momentum
        df['returns'] = df['close'].pct_change()
        df['momentum'] = df['returns'].rolling(window=5).mean()
        
        # Volatility
        df['volatility'] = df['returns'].rolling(window=10).std()
        
        # Volume features
        df['volume_ma'] = df['volume'].rolling(window=10).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Fibonacci level features
        current_price = df['close'].iloc[-1]
        
        # Distance to each Fibonacci level
        for ratio, level in fib_levels.items():
            distance = (current_price - level) / current_price
            features.append(distance)
        
        # Add price features
        features.extend([
            df['momentum'].iloc[-1],
            df['volatility'].iloc[-1],
            df['volume_ratio'].iloc[-1],
            df['returns'].iloc[-1]
        ])
        
        return np.array(features).reshape(1, -1)
    
    def _predict_price_movement(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Predict price movement using the ML model.
        
        Args:
            features: NumPy array of features
            
        Returns:
            Tuple of (predicted_action, confidence)
        """
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
    
    def _execute_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the Fibonacci ML strategy on the given task.
        
        Args:
            task: Dictionary containing market data and parameters
                Expected keys:
                - 'data': DataFrame with OHLCV data
                - 'current_price': Current market price
                - 'symbol': Trading symbol
                - 'timeframe': Timeframe of the data
                
        Returns:
            Dictionary with signal information
        """
        # Extract data from task
        df = task.get('data')
        current_price = task.get('current_price')
        symbol = task.get('symbol', 'BTC')
        timeframe = task.get('timeframe', '1h')
        
        # Validate inputs
        if df is None or current_price is None:
            return {
                'action': 'HOLD',
                'confidence': 0.0,
                'message': 'Missing required data for Fibonacci ML analysis',
                'agent': self.name
            }
        
        # Generate base Fibonacci signal
        base_signal = self.strategy.generate_signal(df, current_price)
        
        # Extract features for ML prediction
        features = self._extract_features(df, base_signal['fib_levels'])
        
        # Predict price movement
        ml_action, ml_confidence = self._predict_price_movement(features)
        
        # Combine base signal and ML prediction
        # If ML confidence is high, use ML prediction
        # Otherwise, use base Fibonacci signal
        if ml_confidence > 0.7:
            action = ml_action
            confidence = ml_confidence
        else:
            action = base_signal['action']
            confidence = base_signal['confidence']
        
        # Create combined signal
        signal = {
            'action': action,
            'confidence': confidence,
            'support_levels': base_signal['support_levels'],
            'resistance_levels': base_signal['resistance_levels'],
            'nearest_support': base_signal['nearest_support'],
            'nearest_resistance': base_signal['nearest_resistance'],
            'fib_levels': base_signal['fib_levels'],
            'ml_prediction': ml_action,
            'ml_confidence': ml_confidence,
            'agent': self.name,
            'symbol': symbol,
            'timeframe': timeframe,
            'strategy': 'Fibonacci ML'
        }
        
        return signal 