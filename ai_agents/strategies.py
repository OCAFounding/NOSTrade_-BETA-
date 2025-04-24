from utils.logger import logger

def shift_to_stablecoins(symbol):
    """
    Strategy to shift assets to stablecoins during high volatility
    """
    logger.info(f"Shifting {symbol} to stablecoins")
    # Implementation would connect to exchange APIs
    return {
        'action': 'sell',
        'symbol': symbol,
        'target': 'USDT',
        'reason': 'high volatility'
    }

def increase_risk_exposure(symbol):
    """
    Strategy to increase risk exposure during bullish markets
    """
    logger.info(f"Increasing risk exposure for {symbol}")
    # Implementation would connect to exchange APIs
    return {
        'action': 'buy',
        'symbol': symbol,
        'leverage': 2,
        'reason': 'bullish trend'
    }

def maintain_allocation(symbol):
    """
    Strategy to maintain current allocation
    """
    logger.info(f"Maintaining current allocation for {symbol}")
    return {
        'action': 'hold',
        'symbol': symbol,
        'reason': 'stable market conditions'
    }

# Strategy registry
STRATEGIES = {
    'shift to stablecoins': shift_to_stablecoins,
    'increase risk exposure': increase_risk_exposure,
    'maintain current allocation': maintain_allocation
} 