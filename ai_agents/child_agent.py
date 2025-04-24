from utils.logger import logger

class ChildAgent:
    def __init__(self, symbol, strategy_functions=None):
        self.symbol = symbol
        self.strategy_functions = strategy_functions or {}
        self.current_position = 0
        self.last_execution = None
        
    def execute_strategy(self, strategy):
        """
        Execute a specific strategy for this agent's symbol
        """
        logger.info(f"Executing strategy '{strategy}' for {self.symbol}")
        
        if strategy in self.strategy_functions:
            try:
                result = self.strategy_functions[strategy](self.symbol)
                self.last_execution = {
                    'strategy': strategy,
                    'result': result,
                    'timestamp': self._get_current_timestamp()
                }
                return result
            except Exception as e:
                logger.error(f"Error executing strategy '{strategy}' for {self.symbol}: {e}")
                return None
        else:
            logger.warning(f"Strategy '{strategy}' not implemented for {self.symbol}")
            return None
            
    def add_strategy(self, name, function):
        """
        Add a new strategy function for this agent
        """
        self.strategy_functions[name] = function
        logger.info(f"Added strategy '{name}' for {self.symbol}")
        
    def get_status(self):
        """
        Get the current status of this agent
        """
        return {
            'symbol': self.symbol,
            'current_position': self.current_position,
            'last_execution': self.last_execution,
            'available_strategies': list(self.strategy_functions.keys())
        }
        
    def _get_current_timestamp(self):
        """
        Get the current timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat() 