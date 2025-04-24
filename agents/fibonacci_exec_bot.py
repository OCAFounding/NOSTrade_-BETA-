from agents.trading_agent import TradingAgent
from typing import Dict, Any, Optional
import pandas as pd
from utils.logger import logger

class FibonacciExecBot:
    """
    Execution bot for Fibonacci-based trading strategies.
    This bot executes trades based on signals from Fibonacci agents.
    """
    
    def __init__(self, trading_agent: Optional[TradingAgent] = None):
        """
        Initialize the Fibonacci execution bot.
        
        Args:
            trading_agent: Trading agent to use for execution (if None, a new one will be created)
        """
        self.trading_agent = trading_agent or TradingAgent()
        logger.info("Fibonacci execution bot initialized")
    
    def execute_signal(self, signal: Dict[str, Any], amount: float = 0.01) -> Dict[str, Any]:
        """
        Execute a trading signal from a Fibonacci agent.
        
        Args:
            signal: Dictionary containing signal information
                Expected keys:
                - 'action': Trading action ('BUY', 'SELL', or 'HOLD')
                - 'confidence': Confidence level of the signal
                - 'symbol': Trading symbol
                - 'agent': Name of the agent that generated the signal
            amount: Amount to trade (in base currency)
            
        Returns:
            Dictionary with execution result
        """
        # Extract signal information
        action = signal.get('action', 'HOLD')
        confidence = signal.get('confidence', 0.0)
        symbol = signal.get('symbol', 'BTC')
        agent = signal.get('agent', 'Unknown')
        
        # Log the signal
        logger.info(f"Received {action} signal from {agent} for {symbol} with confidence {confidence}")
        
        # Check if we should execute the trade
        if action == 'HOLD' or confidence < 0.6:
            logger.info(f"Skipping execution: {action} signal with confidence {confidence}")
            return {
                'executed': False,
                'action': action,
                'symbol': symbol,
                'confidence': confidence,
                'agent': agent,
                'reason': 'Signal confidence too low or HOLD action'
            }
        
        # Execute the trade
        try:
            # Determine the side based on the action
            side = 'BUY' if action == 'BUY' else 'SELL'
            
            # Execute the trade
            result = self.trading_agent.execute_trade(
                symbol=symbol,
                side=side,
                qty=amount,
                exchange='binance'  # Default to Binance
            )
            
            # Log the execution
            logger.info(f"Executed {side} trade for {symbol}: {result}")
            
            # Return the execution result
            return {
                'executed': True,
                'action': action,
                'symbol': symbol,
                'confidence': confidence,
                'agent': agent,
                'result': result
            }
            
        except Exception as e:
            # Log the error
            logger.error(f"Error executing {action} trade for {symbol}: {e}")
            
            # Return the error
            return {
                'executed': False,
                'action': action,
                'symbol': symbol,
                'confidence': confidence,
                'agent': agent,
                'error': str(e)
            }
    
    def execute_signals(self, signals: list, amount: float = 0.01) -> list:
        """
        Execute multiple trading signals.
        
        Args:
            signals: List of signal dictionaries
            amount: Amount to trade for each signal (in base currency)
            
        Returns:
            List of execution results
        """
        results = []
        
        for signal in signals:
            result = self.execute_signal(signal, amount)
            results.append(result)
        
        return results 