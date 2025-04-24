import time
import logging
from typing import Dict, Any, Optional

# Import our adapter factory for Fibonacci signals
from fibonacci_modules.adapter_factory import FibonacciAdapterFactory

# Import the fibonacci_agent functions
from fibonacci_agent import ensemble_fibonacci_signal

# Import AI agent and trade executor
from ai_agent_parent import ParentAI
from trading_bot_executor import TradeExecutor

class SignalRouter:
    """
    SignalRouter class that integrates Fibonacci ensemble signals with the parent AI agent
    and trade executor for real-time signal processing and execution.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SignalRouter with the parent AI agent and trade executor.
        
        Args:
            config_path: Optional path to the configuration file for the Fibonacci adapter factory
        """
        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Initialize components
        self.logger.info("Initializing SignalRouter components...")
        self.parent_agent = ParentAI()
        self.trade_executor = TradeExecutor()
        
        # Initialize Fibonacci adapter factory
        self.fibonacci_factory = FibonacciAdapterFactory(config_path)
        self.logger.info("SignalRouter initialization complete")
        
    def process_signal(self):
        """
        Process signals from the Fibonacci ensemble, analyze with parent AI,
        and execute trades if necessary.
        """
        try:
            # Get market data (placeholder - replace with actual market data source)
            market_data = self._get_market_data()
            
            # Option 1: Use our adapter system
            self.logger.info("[Router] Gathering market signal from Fibonacci Adapter System...")
            adapter_signal = self.fibonacci_factory.get_signal(market_data)
            self.logger.info(f"[Router] Received adapter signal: {adapter_signal['action']}, Confidence: {adapter_signal['confidence']:.2f}")
            
            # Option 2: Use the fibonacci_agent directly
            self.logger.info("[Router] Gathering market signal from Fibonacci Ensemble...")
            ensemble_signal = ensemble_fibonacci_signal()
            self.logger.info(f"[Router] Received ensemble signal: {ensemble_signal}")
            
            # Combine signals for more robust decision making
            combined_signal = self._combine_signals(adapter_signal, ensemble_signal)
            self.logger.info(f"[Router] Combined signal: {combined_signal}")
            
            # Analyze signal with parent AI
            decision = self.parent_agent.analyze_signal(combined_signal)
            self.logger.info(f"[Router] Parent AI decision: {decision}")
            
            # Execute trade if necessary
            if decision in ["BUY", "SELL"]:
                self.logger.info(f"[Router] Executing {decision} order...")
                self.trade_executor.execute_order(decision)
            else:
                self.logger.info("[Router] Holding position. No action taken.")
                
        except Exception as e:
            self.logger.error(f"[Router] Error processing signal: {str(e)}")
            
    def _get_market_data(self) -> Dict[str, Any]:
        """
        Get market data from the data source.
        
        Returns:
            Dictionary containing market data (OHLCV, etc.)
        """
        # This is a placeholder - replace with actual market data source
        # For now, we'll use the get_market_data function from fibonacci_agent
        from fibonacci_agent import get_market_data
        return get_market_data()
        
    def _combine_signals(self, adapter_signal: Dict[str, Any], ensemble_signal: str) -> Dict[str, Any]:
        """
        Combine signals from the adapter system and the fibonacci_agent.
        
        Args:
            adapter_signal: Signal from the adapter system
            ensemble_signal: Signal from the fibonacci_agent
            
        Returns:
            Combined signal dictionary
        """
        # Map ensemble signal to our format
        ensemble_action = ensemble_signal.lower()
        
        # Create a combined signal
        combined_signal = {
            'action': adapter_signal['action'],
            'confidence': adapter_signal['confidence'],
            'ensemble_signal': ensemble_action,
            'adapter_signal': adapter_signal['action'],
            'adapter_confidence': adapter_signal['confidence']
        }
        
        # If signals agree, increase confidence
        if adapter_signal['action'] == ensemble_action:
            combined_signal['confidence'] = min(1.0, adapter_signal['confidence'] + 0.2)
            
        return combined_signal

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize and run the signal router
    router = SignalRouter()
    
    # Run continuously
    while True:
        router.process_signal()
        time.sleep(60)  # Check every minute 