import numpy as np
import json
import os
from adapter_factory import FibonacciAdapterFactory
from ensemble_adapter import EnsembleFibonacciAdapter

def generate_test_data(num_points=100):
    """Generate test market data."""
    np.random.seed(42)  # For reproducibility
    
    # Generate price data with a slight upward trend
    base_price = 100
    trend = np.linspace(0, 5, num_points)
    noise = np.random.normal(0, 1, num_points)
    
    close = base_price + trend + noise
    high = close + np.random.uniform(0.5, 1.5, num_points)
    low = close - np.random.uniform(0.5, 1.5, num_points)
    
    return {
        "close": close.tolist(),
        "high": high.tolist(),
        "low": low.tolist(),
        "volume": np.random.uniform(1000, 5000, num_points).tolist()
    }

def test_ensemble_adapter():
    """Test the ensemble adapter directly."""
    print("Testing Ensemble Adapter directly...")
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Create ensemble adapter
    ensemble_config = config.get('ensemble', {})
    adapter = EnsembleFibonacciAdapter(ensemble_config)
    
    # Generate test data
    market_data = generate_test_data()
    
    # Get Fibonacci levels
    levels = adapter.get_levels(market_data)
    print(f"Ensemble Support: {levels['support']}")
    print(f"Ensemble Resistance: {levels['resistance']}")
    print(f"Individual Support Levels: {levels['support_levels']}")
    print(f"Individual Resistance Levels: {levels['resistance_levels']}")
    
    # Get trading signal
    current_price = market_data['close'][-1]
    signal, confidence = adapter.get_signal(market_data, current_price)
    print(f"Signal: {signal}, Confidence: {confidence:.2f}")

def test_adapter_factory():
    """Test the adapter factory with the ensemble adapter."""
    print("\nTesting Adapter Factory with Ensemble Adapter...")
    
    # Create adapter factory
    factory = FibonacciAdapterFactory()
    
    # Generate test data
    market_data = generate_test_data()
    
    # Get levels from all adapters
    levels = factory.get_levels(market_data)
    print(f"Factory Support: {levels['support']}")
    print(f"Factory Resistance: {levels['resistance']}")
    
    # Get signal from all adapters
    signal = factory.get_signal(market_data)
    print(f"Factory Signal: {signal['action']}, Confidence: {signal['confidence']:.2f}")
    
    # Get signal from ensemble adapter only
    ensemble_signal = factory.get_signal(market_data, adapter_name='ensemble')
    print(f"Ensemble Signal: {ensemble_signal['action']}, Confidence: {ensemble_signal['confidence']:.2f}")

if __name__ == "__main__":
    test_ensemble_adapter()
    test_adapter_factory() 