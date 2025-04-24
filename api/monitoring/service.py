from typing import Dict, Any, List, Optional
import logging
import random
from datetime import datetime, timedelta
from .config import get_monitoring_config
import uuid

class MonitoringService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = get_monitoring_config()
        
        # Initialize data storage
        self._signals: List[Dict[str, Any]] = []
        self._confidences: List[Dict[str, Any]] = []
        self._alerts: List[Dict[str, Any]] = []
        
        # Track last update time
        self._last_update = datetime.min
        
    def get_latest_data(self) -> Dict[str, Any]:
        """
        Get the latest monitoring data, updating if necessary.
        
        Returns:
            Dict[str, Any]: Latest monitoring data
        """
        if self._should_update():
            self._update_data()
            
        return {
            "signals": self._signals,
            "confidences": self._confidences,
            "alerts": self._alerts
        }
        
    def add_alert(self, title: str, description: str, level: str) -> None:
        """
        Add a new alert to the system.
        
        Args:
            title: Alert title
            description: Alert description
            level: Alert level (info, warning, error, critical)
        """
        alert = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "level": level,
            "timestamp": datetime.now(),
            "source": "monitoring_service"
        }
        
        self._alerts.append(alert)
        self._cleanup_alerts()
        
        self.logger.info(f"Added new alert: {title} ({level})")
        
    def _should_update(self) -> bool:
        """
        Check if data should be updated based on the update interval.
        
        Returns:
            bool: True if update is needed
        """
        return (datetime.now() - self._last_update).total_seconds() >= self.config["update_interval"]
        
    def _update_data(self) -> None:
        """
        Update the monitoring data with new values.
        In a production environment, this would fetch real data from various sources.
        """
        self._update_signals()
        self._update_confidences()
        self._check_for_alerts()
        self._last_update = datetime.now()
        
    def _update_signals(self) -> None:
        """
        Update the signals data.
        This is a mock implementation that generates random signals.
        """
        # Keep only the latest signals up to max_signals
        if len(self._signals) >= self.config["max_signals"]:
            self._signals = self._signals[-self.config["max_signals"]:]
            
        # Generate a new random signal
        actions = ["BUY", "SELL", "HOLD"]
        assets = ["BTC", "ETH", "SOL"]
        
        new_signal = {
            "id": str(uuid.uuid4()),
            "asset": random.choice(assets),
            "action": random.choice(actions),
            "confidence": random.uniform(0.5, 1.0),
            "timestamp": datetime.now(),
            "source": "mock_signal_generator"
        }
        
        self._signals.append(new_signal)
        
    def _update_confidences(self) -> None:
        """
        Update the confidence metrics data.
        This is a mock implementation that generates random confidence values.
        """
        # Keep only the latest confidences up to max_confidences
        if len(self._confidences) >= self.config["max_confidences"]:
            self._confidences = self._confidences[-self.config["max_confidences"]:]
            
        # Generate a new random confidence metric
        new_confidence = {
            "timestamp": datetime.now(),
            "value": random.uniform(0.5, 1.0),
            "source": "mock_confidence_generator"
        }
        
        self._confidences.append(new_confidence)
        
    def _check_for_alerts(self) -> None:
        """
        Check current data for conditions that should trigger alerts.
        This is a mock implementation that randomly generates alerts.
        """
        if random.random() < 0.1:  # 10% chance of generating an alert
            alert_levels = ["info", "warning", "error", "critical"]
            alert_titles = [
                "High Volatility Detected",
                "Low Confidence Signal",
                "Multiple Conflicting Signals",
                "System Performance Warning"
            ]
            
            self.add_alert(
                title=random.choice(alert_titles),
                description="This is a mock alert for testing purposes.",
                level=random.choice(alert_levels)
            )
            
    def _cleanup_alerts(self) -> None:
        """
        Remove old alerts based on the max_alerts configuration.
        """
        if len(self._alerts) > self.config["max_alerts"]:
            self._alerts = self._alerts[-self.config["max_alerts"]:] 