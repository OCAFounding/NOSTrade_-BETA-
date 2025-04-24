import logging
import time
from typing import Dict, Any, Optional, List
import json
import os

class TradeExecutor:
    """
    TradeExecutor class that executes trading orders based on signals.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the TradeExecutor.
        
        Args:
            config_path: Optional path to the configuration file
        """
        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize trade history
        self.trade_history = []
        self.max_history_size = self.config.get('max_trade_history', 1000)
        
        # Initialize trade parameters
        self.default_symbol = self.config.get('default_symbol', 'BTC')
        self.default_amount = self.config.get('default_amount', 0.01)
        self.max_slippage = self.config.get('max_slippage', 0.02)  # 2% max slippage
        
        self.logger.info("TradeExecutor initialized")
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dictionary containing configuration
        """
        # Default configuration
        default_config = {
            'default_symbol': 'BTC',
            'default_amount': 0.01,
            'max_slippage': 0.02,
            'max_trade_history': 1000,
            'simulation_mode': True
        }
        
        # If no config path provided, use default
        if config_path is None:
            return default_config
            
        # Try to load from file
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            # Merge with default config
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                    
            return config
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.warning(f"Error loading configuration: {str(e)}. Using default configuration.")
            return default_config
            
    def execute_order(self, action: str, symbol: Optional[str] = None, amount: Optional[float] = None) -> bool:
        """
        Execute a trading order.
        
        Args:
            action: Trading action ("BUY" or "SELL")
            symbol: Trading symbol (optional)
            amount: Trading amount (optional)
            
        Returns:
            Boolean indicating success
        """
        try:
            # Use defaults if not provided
            symbol = symbol or self.default_symbol
            amount = amount or self.default_amount
            
            # Validate action
            if action not in ["BUY", "SELL"]:
                self.logger.error(f"Invalid action: {action}")
                return False
                
            # Check if in simulation mode
            if self.config.get('simulation_mode', True):
                return self._simulate_order(action, symbol, amount)
            else:
                return self._execute_real_order(action, symbol, amount)
                
        except Exception as e:
            self.logger.error(f"Error executing order: {str(e)}")
            return False
            
    def _simulate_order(self, action: str, symbol: str, amount: float) -> bool:
        """
        Simulate a trading order.
        
        Args:
            action: Trading action ("BUY" or "SELL")
            symbol: Trading symbol
            amount: Trading amount
            
        Returns:
            Boolean indicating success
        """
        # Simulate order execution delay
        time.sleep(0.5)
        
        # Generate a simulated price with some randomness
        import random
        base_price = 50000  # Example base price
        price_variation = random.uniform(-0.01, 0.01)  # ±1% variation
        execution_price = base_price * (1 + price_variation)
        
        # Calculate slippage
        slippage = abs(price_variation)
        if slippage > self.max_slippage:
            self.logger.warning(f"Simulated slippage {slippage:.2%} exceeds maximum {self.max_slippage:.2%}")
            return False
            
        # Record the trade
        trade = {
            'timestamp': time.time(),
            'action': action,
            'symbol': symbol,
            'amount': amount,
            'price': execution_price,
            'slippage': slippage,
            'status': 'success'
        }
        
        self._add_to_history(trade)
        
        # Log the trade
        self.logger.info(f"Simulated {action} order executed: {amount} {symbol} at {execution_price:.2f} (slippage: {slippage:.2%})")
        
        return True
        
    def _execute_real_order(self, action: str, symbol: str, amount: float) -> bool:
        """
        Execute a real trading order.
        
        Args:
            action: Trading action ("BUY" or "SELL")
            symbol: Trading symbol
            amount: Trading amount
            
        Returns:
            Boolean indicating success
        """
        # This is a placeholder for real order execution
        # In a real implementation, this would connect to a broker/exchange API
        
        self.logger.info(f"Executing real {action} order: {amount} {symbol}")
        
        # Record the trade
        trade = {
            'timestamp': time.time(),
            'action': action,
            'symbol': symbol,
            'amount': amount,
            'status': 'pending'
        }
        
        self._add_to_history(trade)
        
        # Simulate order execution
        time.sleep(1)
        
        # Update trade status
        trade['status'] = 'success'
        trade['price'] = 50000  # Example price
        
        self.logger.info(f"Real {action} order executed: {amount} {symbol}")
        
        return True
        
    def _add_to_history(self, trade: Dict[str, Any]):
        """
        Add trade to history, maintaining the maximum history size.
        
        Args:
            trade: Trade to add to history
        """
        self.trade_history.append(trade)
        
        # Trim history if it exceeds the maximum size
        if len(self.trade_history) > self.max_history_size:
            self.trade_history = self.trade_history[-self.max_history_size:]
            
    def get_trade_history(self) -> List[Dict[str, Any]]:
        """
        Get the trade history.
        
        Returns:
            List of historical trades
        """
        return self.trade_history.copy()
        
    def get_position(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the current position for a symbol.
        
        Args:
            symbol: Trading symbol (optional)
            
        Returns:
            Dictionary containing position information
        """
        symbol = symbol or self.default_symbol
        
        # Calculate position from trade history
        position = 0.0
        for trade in self.trade_history:
            if trade['symbol'] == symbol:
                if trade['action'] == 'BUY':
                    position += trade['amount']
                elif trade['action'] == 'SELL':
                    position -= trade['amount']
                    
        return {
            'symbol': symbol,
            'position': position,
            'timestamp': time.time()
        }
        
    def reset_history(self):
        """Reset the trade history."""
        self.trade_history = []
        self.logger.info("Trade history reset") 