from typing import Dict, Any

# Default monitoring settings
DEFAULT_MONITORING_CONFIG = {
    # Update settings
    "update_interval": 10,  # 10 seconds
    "max_signals": 20,  # Maximum number of signals to keep
    "max_confidences": 10,  # Maximum number of confidence metrics to keep
    "max_alerts": 50,  # Maximum number of alerts to keep
    
    # Alert thresholds
    "alert_thresholds": {
        "confidence": {
            "warning": 70,  # Warning if confidence below 70%
            "error": 50     # Error if confidence below 50%
        },
        "volatility": {
            "warning": 0.02,  # Warning if volatility above 2%
            "error": 0.05     # Error if volatility above 5%
        },
        "signal_conflict": {
            "warning": 2,  # Warning if 2 conflicting signals
            "error": 3      # Error if 3 or more conflicting signals
        }
    },
    
    # Visualization settings
    "chart_settings": {
        "confidence_colors": {
            "high": "rgba(75, 192, 192, 0.6)",
            "medium": "rgba(255, 206, 86, 0.6)",
            "low": "rgba(255, 99, 132, 0.6)"
        },
        "signal_colors": {
            "BUY": "rgba(75, 192, 192, 0.6)",
            "SELL": "rgba(255, 99, 132, 0.6)",
            "HOLD": "rgba(54, 162, 235, 0.6)"
        },
        "alert_colors": {
            "info": "rgba(54, 162, 235, 0.6)",
            "warning": "rgba(255, 206, 86, 0.6)",
            "error": "rgba(255, 99, 132, 0.6)",
            "critical": "rgba(153, 102, 255, 0.6)"
        }
    },
    
    # Notification settings
    "notifications": {
        "enabled": True,
        "channels": ["email", "slack"],
        "recipients": {
            "email": ["monitoring@example.com"],
            "slack": ["#trading-alerts"]
        },
        "alert_levels": ["error", "critical"]  # Only notify for these levels
    },
    
    # Logging settings
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

def get_monitoring_config() -> Dict[str, Any]:
    """
    Get the monitoring configuration.
    In a production environment, this would load from a database or config file.
    
    Returns:
        Dict[str, Any]: Monitoring configuration
    """
    return DEFAULT_MONITORING_CONFIG.copy()

def update_monitoring_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the monitoring configuration.
    In a production environment, this would persist to a database or config file.
    
    Args:
        new_config: New configuration values to update
        
    Returns:
        Dict[str, Any]: Updated monitoring configuration
    """
    config = get_monitoring_config()
    config.update(new_config)
    return config 