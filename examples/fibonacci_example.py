import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.fibonacci_agent import FibonacciAgent
from agents.fibonacci_ml_agent import FibonacciMLAgent
from agents.fibonacci_exec_bot import FibonacciExecBot
from utils.logger import logger

def generate_sample_data(days=30, interval='1h'):
    """
    Generate sample price data for testing.
    
    Args:
        days: Number of days of data to generate
        interval: Time interval ('1h', '4h', '1d')
        
    Returns:
        DataFrame with OHLCV data
    """
    # Calculate the number of intervals
    if interval == '1h':
        intervals = days * 24
    elif interval == '4h':
        intervals = days * 6
    else:  # 1d
        intervals = days
    
    # Generate timestamps
    end_time = datetime.now()
    if interval == '1h':
        start_time = end_time - timedelta(hours=intervals)
        timestamps = [start_time + timedelta(hours=i) for i in range(intervals)]
    elif interval == '4h':
        start_time = end_time - timedelta(hours=intervals*4)
        timestamps = [start_time + timedelta(hours=i*4) for i in range(intervals)]
    else:  # 1d
        start_time = end_time - timedelta(days=intervals)
        timestamps = [start_time + timedelta(days=i) for i in range(intervals)]
    
    # Generate price data
    base_price = 50000  # Starting price
    volatility = 0.02   # Daily volatility
    
    # Generate random walk
    np.random.seed(42)
    returns = np.random.normal(0, volatility/np.sqrt(24 if interval == '1h' else 6 if interval == '4h' else 1), intervals)
    prices = base_price * (1 + returns).cumprod()
    
    # Add some Fibonacci-like patterns
    for i in range(0, intervals, 20):
        if i + 20 < intervals:
            # Create a swing high
            prices[i+10] = prices[i+10] * 1.05
            # Create a swing low
            prices[i+15] = prices[i+15] * 0.95
    
    # Generate OHLCV data
    data = []
    for i, timestamp in enumerate(timestamps):
        price = prices[i]
        high = price * (1 + np.random.uniform(0, 0.01))
        low = price * (1 - np.random.uniform(0, 0.01))
        open_price = low + (high - low) * np.random.uniform(0.3, 0.7)
        close = low + (high - low) * np.random.uniform(0.3, 0.7)
        volume = np.random.uniform(100, 1000)
        
        data.append({
            'timestamp': timestamp,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    
    return df

def main():
    # Generate sample data
    logger.info("Generating sample data...")
    df = generate_sample_data(days=30, interval='1h')
    
    # Get current price
    current_price = df['close'].iloc[-1]
    
    # Create task for agents
    task = {
        'data': df,
        'current_price': current_price,
        'symbol': 'BTC',
        'timeframe': '1h'
    }
    
    # Initialize agents
    logger.info("Initializing Fibonacci agents...")
    fib_agent = FibonacciAgent(name="BasicFibonacci")
    fib_ml_agent = FibonacciMLAgent(name="MLFibonacci")
    
    # Get signals from agents
    logger.info("Getting signals from agents...")
    fib_signal = fib_agent.receive_task(task)
    fib_ml_signal = fib_ml_agent.receive_task(task)
    
    # Print signals
    logger.info(f"Basic Fibonacci signal: {fib_signal['action']} with confidence {fib_signal['confidence']}")
    logger.info(f"ML Fibonacci signal: {fib_ml_signal['action']} with confidence {fib_ml_signal['confidence']}")
    
    # Initialize execution bot
    logger.info("Initializing Fibonacci execution bot...")
    exec_bot = FibonacciExecBot()
    
    # Execute signals (in a real scenario, you would only execute one of them)
    logger.info("Executing signals...")
    results = exec_bot.execute_signals([fib_signal, fib_ml_signal], amount=0.001)
    
    # Print results
    for i, result in enumerate(results):
        agent_name = "Basic Fibonacci" if i == 0 else "ML Fibonacci"
        if result['executed']:
            logger.info(f"{agent_name} signal executed: {result['action']} for {result['symbol']}")
        else:
            logger.info(f"{agent_name} signal not executed: {result.get('reason', 'Unknown reason')}")

if __name__ == "__main__":
    main() 