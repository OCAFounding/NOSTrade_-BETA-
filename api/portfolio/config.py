from typing import Dict, Any

# Default portfolio settings
DEFAULT_PORTFOLIO_CONFIG = {
    # Optimization settings
    "optimization_interval": 3600,  # 1 hour in seconds
    "min_allocation": 0.05,  # 5% minimum allocation
    "max_allocation": 0.40,  # 40% maximum allocation
    
    # Risk settings
    "target_volatility": 0.20,  # 20% target portfolio volatility
    "risk_free_rate": 0.02,  # 2% risk-free rate for Sharpe ratio
    "max_drawdown": 0.15,  # 15% maximum drawdown
    
    # Yield settings
    "min_yield": 0.03,  # 3% minimum yield
    "max_yield": 0.15,  # 15% maximum yield
    "yield_update_interval": 300,  # 5 minutes in seconds
    
    # Asset settings
    "supported_assets": [
        "BTC", "ETH", "SOL", "AVAX", "DOT"
    ],
    "asset_weights": {
        "BTC": 1.0,
        "ETH": 0.9,
        "SOL": 0.8,
        "AVAX": 0.7,
        "DOT": 0.6
    },
    
    # Optimization constraints
    "constraints": {
        "min_assets": 3,  # Minimum number of assets in portfolio
        "max_assets": 5,  # Maximum number of assets in portfolio
        "rebalance_threshold": 0.05  # 5% threshold for rebalancing
    }
}

def get_portfolio_config() -> Dict[str, Any]:
    """
    Get the portfolio configuration.
    In a production environment, this would load from a database or config file.
    
    Returns:
        Dict[str, Any]: Portfolio configuration
    """
    return DEFAULT_PORTFOLIO_CONFIG.copy()

def update_portfolio_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the portfolio configuration.
    In a production environment, this would persist to a database or config file.
    
    Args:
        new_config: New configuration values to update
        
    Returns:
        Dict[str, Any]: Updated portfolio configuration
    """
    config = get_portfolio_config()
    config.update(new_config)
    return config 