import numpy as np
import json
import os
from adapter_factory import FibonacciAdapterFactory
from ensemble_adapter import EnsembleFibonacciAdapter

# Import the fibonacci_agent.py functions
from fibonacci_agent import (
    get_market_data,
    fib_strategy_harshgupta,
    fib_strategy_brandon,
    fib_strategy_ranjit,
    fib_strategy_joengelh,
    fib_strategy_faraway,
    fib_strategy_nerr,
    fib_strategy_doombringer,
    fibonacci_ensemble,
    generate_signal
)

def compare_approaches():
    """Compare the fibonacci_agent.py approach with our adapter system."""
    print("Comparing fibonacci_agent.py with adapter system...")
    
    # Get market data using the fibonacci_agent.py function
    market_data = get_market_data()
    
    # === Approach 1: Direct use of fibonacci_agent.py ===
    print("\n=== Approach 1: Direct use of fibonacci_agent.py ===")
    
    # Get ensemble levels
    ensemble_levels = fibonacci_ensemble(market_data)
    print(f"fibonacci_agent.py Ensemble Support: {ensemble_levels['support']}")
    print(f"fibonacci_agent.py Ensemble Resistance: {ensemble_levels['resistance']}")
    
    # Get signal
    signal = generate_signal(market_data)
    print(f"fibonacci_agent.py Signal: {signal}")
    
    # === Approach 2: Use our adapter system ===
    print("\n=== Approach 2: Use our adapter system ===")
    
    # Create adapter factory
    factory = FibonacciAdapterFactory()
    
    # Get levels from all adapters
    adapter_levels = factory.get_levels(market_data)
    print(f"Adapter System Support: {adapter_levels['support']}")
    print(f"Adapter System Resistance: {adapter_levels['resistance']}")
    
    # Get signal from all adapters
    adapter_signal = factory.get_signal(market_data)
    print(f"Adapter System Signal: {adapter_signal['action']}, Confidence: {adapter_signal['confidence']:.2f}")
    
    # === Approach 3: Use ensemble adapter directly ===
    print("\n=== Approach 3: Use ensemble adapter directly ===")
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Create ensemble adapter
    ensemble_config = config.get('ensemble', {})
    adapter = EnsembleFibonacciAdapter(ensemble_config)
    
    # Get Fibonacci levels
    levels = adapter.get_levels(market_data)
    print(f"Ensemble Adapter Support: {levels['support']}")
    print(f"Ensemble Adapter Resistance: {levels['resistance']}")
    
    # Get trading signal
    current_price = market_data['close'][-1]
    signal, confidence = adapter.get_signal(market_data, current_price)
    print(f"Ensemble Adapter Signal: {signal}, Confidence: {confidence:.2f}")

def demonstrate_integration():
    """Demonstrate how to integrate the fibonacci_agent.py approach with our adapter system."""
    print("\n=== Demonstrating Integration ===")
    
    # Get market data
    market_data = get_market_data()
    
    # Create a custom adapter that uses the fibonacci_agent.py approach
    class CustomFibonacciAdapter(EnsembleFibonacciAdapter):
        """Custom adapter that uses the fibonacci_agent.py approach."""
        
        def get_levels(self, market_data):
            """Use the fibonacci_ensemble function from fibonacci_agent.py."""
            result = fibonacci_ensemble(market_data)
            
            # Convert to our adapter format
            return {
                'support': [result['support']],
                'resistance': [result['resistance']],
                'support_levels': [result['support']],
                'resistance_levels': [result['resistance']],
                'strategies_used': result['strategies_used']
            }
        
        def get_signal(self, market_data, current_price):
            """Use the generate_signal function from fibonacci_agent.py."""
            signal = generate_signal(market_data)
            
            # Convert to our adapter format
            if signal == "BUY":
                return 'buy', 0.8
            elif signal == "SELL":
                return 'sell', 0.8
            else:
                return 'hold', 0.0
    
    # Create custom adapter
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    custom_config = config.get('ensemble', {})
    custom_adapter = CustomFibonacciAdapter(custom_config)
    
    # Get Fibonacci levels
    levels = custom_adapter.get_levels(market_data)
    print(f"Custom Adapter Support: {levels['support']}")
    print(f"Custom Adapter Resistance: {levels['resistance']}")
    
    # Get trading signal
    current_price = market_data['close'][-1]
    signal, confidence = custom_adapter.get_signal(market_data, current_price)
    print(f"Custom Adapter Signal: {signal}, Confidence: {confidence:.2f}")

if __name__ == "__main__":
    compare_approaches()
    demonstrate_integration() 