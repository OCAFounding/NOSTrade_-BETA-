from agents.child_agent import ChildAgent
from strategies.fibonacci_strategy import FibonacciStrategy
import pandas as pd
from typing import Dict, Any

class FibonacciAgent(ChildAgent):
    """
    Child agent that specializes in Fibonacci retracement analysis.
    This agent uses Fibonacci retracement levels to identify potential
    support and resistance levels and generate trading signals.
    """
    
    def __init__(self, name: str = "FibonacciAgent", lookback_period: int = 100):
        """
        Initialize the Fibonacci agent.
        
        Args:
            name: Name of the agent
            lookback_period: Number of candles to look back for swing highs/lows
        """
        # Create the Fibonacci strategy
        strategy = FibonacciStrategy(lookback_period=lookback_period)
        
        # Initialize the child agent with the strategy function
        super().__init__(name, self._execute_strategy)
        
        # Store the strategy instance
        self.strategy = strategy
        
    def _execute_strategy(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the Fibonacci strategy on the given task.
        
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
                'message': 'Missing required data for Fibonacci analysis',
                'agent': self.name
            }
        
        # Generate signal using the strategy
        signal = self.strategy.generate_signal(df, current_price)
        
        # Add metadata to the signal
        signal['agent'] = self.name
        signal['symbol'] = symbol
        signal['timeframe'] = timeframe
        signal['strategy'] = 'Fibonacci Retracement'
        
        return signal 