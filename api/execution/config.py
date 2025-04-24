from typing import Dict, Any

# Default execution settings
DEFAULT_EXECUTION_CONFIG = {
    # Signal settings
    "signal_update_interval": 60,  # 1 minute in seconds
    "signal_expiry_minutes": 30,  # Signals expire after 30 minutes
    "min_confidence": 70,  # Minimum confidence level for execution
    
    # Execution settings
    "max_retries": 3,  # Maximum number of execution retries
    "retry_delay": 5,  # Delay between retries in seconds
    "execution_timeout": 30,  # Execution timeout in seconds
    
    # Risk settings
    "max_position_size": 1.0,  # Maximum position size in BTC
    "max_daily_trades": 20,  # Maximum number of trades per day
    "max_drawdown": 0.05,  # 5% maximum drawdown
    
    # Notification settings
    "notifications": {
        "enabled": True,
        "channels": ["email", "slack"],
        "recipients": {
            "email": ["trading@example.com"],
            "slack": ["#trading-alerts"]
        }
    },
    
    # Logging settings
    "max_status_entries": 100,  # Maximum number of status entries to keep
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

def get_execution_config() -> Dict[str, Any]:
    """
    Get the execution configuration.
    In a production environment, this would load from a database or config file.
    
    Returns:
        Dict[str, Any]: Execution configuration
    """
    return DEFAULT_EXECUTION_CONFIG.copy()

def update_execution_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the execution configuration.
    In a production environment, this would persist to a database or config file.
    
    Args:
        new_config: New configuration values to update
        
    Returns:
        Dict[str, Any]: Updated execution configuration
    """
    config = get_execution_config()
    config.update(new_config)
    return config 