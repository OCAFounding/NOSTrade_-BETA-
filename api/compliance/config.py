from typing import Dict, Any

# Default compliance settings
DEFAULT_COMPLIANCE_CONFIG = {
    # Logging settings
    "max_log_entries": 1000,
    "log_retention_days": 30,
    
    # Compliance check intervals (in seconds)
    "check_interval": 300,  # 5 minutes
    "emergency_check_interval": 60,  # 1 minute
    
    # Alert thresholds
    "alert_thresholds": {
        "warning": 0.8,  # 80% of limit
        "critical": 0.9,  # 90% of limit
        "emergency": 0.95  # 95% of limit
    },
    
    # Notification settings
    "notifications": {
        "enabled": True,
        "channels": ["email", "slack"],
        "recipients": {
            "email": ["compliance@example.com"],
            "slack": ["#compliance-alerts"]
        }
    },
    
    # Compliance categories and their weights
    "category_weights": {
        "risk": 1.0,
        "position": 0.8,
        "trade": 0.6,
        "leverage": 0.7,
        "general": 0.3
    },
    
    # Compliance score calculation
    "score_calculation": {
        "base_score": 100,
        "violation_penalty": 10,
        "warning_penalty": 5,
        "error_penalty": 15
    }
}

def get_compliance_config() -> Dict[str, Any]:
    """
    Get the compliance configuration.
    In a production environment, this would load from a database or config file.
    
    Returns:
        Dict[str, Any]: Compliance configuration
    """
    return DEFAULT_COMPLIANCE_CONFIG.copy()

def update_compliance_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the compliance configuration.
    In a production environment, this would persist to a database or config file.
    
    Args:
        new_config: New configuration values to update
        
    Returns:
        Dict[str, Any]: Updated compliance configuration
    """
    config = get_compliance_config()
    config.update(new_config)
    return config 