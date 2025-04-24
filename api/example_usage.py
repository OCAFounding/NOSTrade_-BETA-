from decision_client import DecisionClient
import time

def main():
    # Initialize the client
    client = DecisionClient()
    
    # Example market text
    market_text = """
    Bitcoin (BTC) is showing strong bullish momentum with increasing volume.
    Technical indicators suggest a potential breakout above the $50,000 resistance level.
    Market sentiment is positive with growing institutional adoption.
    """
    
    # Execute a trade decision
    print("Executing trade decision...")
    result = client.execute_trade_decision(
        market_text=market_text,
        symbol="BTC",
        amount=0.1
    )
    
    if result:
        print(f"Trade executed: {result}")
    
    # Wait a moment
    time.sleep(1)
    
    # Get current holdings
    print("\nGetting current holdings...")
    holdings = client.get_holdings()
    if holdings:
        print(f"Current holdings: {holdings}")
    
    # Get trade history
    print("\nGetting trade history...")
    history = client.get_trade_history()
    if history:
        print(f"Trade history: {history}")

if __name__ == "__main__":
    main() 