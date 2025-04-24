from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging
from pydantic import BaseModel
from datetime import datetime

from .service import MonitoringService
from .config import get_monitoring_config

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create router
router = APIRouter()

# Initialize monitoring service
monitoring_service = MonitoringService()

# Pydantic models for request/response
class Signal(BaseModel):
    id: str
    asset: str
    action: str
    confidence: float
    timestamp: datetime
    source: str

class ConfidenceMetric(BaseModel):
    timestamp: datetime
    value: float
    source: str

class Alert(BaseModel):
    id: str
    title: str
    description: str
    level: str
    timestamp: datetime
    source: str

class MonitoringData(BaseModel):
    signals: List[Signal]
    confidences: List[ConfidenceMetric]
    alerts: List[Alert]

@router.get("/api/monitoring/latest", response_model=MonitoringData)
async def get_latest_data():
    """
    Get the latest monitoring data including signals, confidence metrics, and alerts.
    
    Returns:
        MonitoringData: Latest monitoring data
    """
    try:
        data = monitoring_service.get_latest_data()
        return MonitoringData(**data)
    except Exception as e:
        logger.error(f"Error getting latest monitoring data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/monitoring/alerts", response_model=Alert)
async def add_alert(alert: Alert):
    """
    Add a new alert to the monitoring system.
    
    Args:
        alert: Alert to add
        
    Returns:
        Alert: Added alert
    """
    try:
        monitoring_service.add_alert(
            title=alert.title,
            description=alert.description,
            level=alert.level
        )
        return alert
    except Exception as e:
        logger.error(f"Error adding alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/monitoring/config", response_model=Dict[str, Any])
async def get_config():
    """
    Get the current monitoring configuration.
    
    Returns:
        Dict[str, Any]: Current monitoring configuration
    """
    try:
        return get_monitoring_config()
    except Exception as e:
        logger.error(f"Error getting monitoring config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 