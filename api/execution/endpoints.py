from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
from pydantic import BaseModel
from .service import ExecutionService

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create router
router = APIRouter()

# Initialize service
execution_service = ExecutionService()

class Signal(BaseModel):
    """Model for a trade signal"""
    id: str
    asset: str
    action: str
    confidence: float
    timestamp: str
    expiry: str

class ExecutionStatus(BaseModel):
    """Model for execution status"""
    id: str
    signal_id: str
    asset: str
    action: str
    message: str
    timestamp: str
    details: Dict[str, Any] = {}
    error: str = None

class FinalDecisionsResponse(BaseModel):
    """Response model for final decisions endpoint"""
    signals: List[Signal]
    status: List[ExecutionStatus]

class ExecuteRequest(BaseModel):
    """Request model for execute endpoint"""
    id: str

class ExecuteResponse(BaseModel):
    """Response model for execute endpoint"""
    success: bool
    message: str
    execution_id: str = None

@router.get("/api/execution/final-decisions", response_model=FinalDecisionsResponse)
async def get_final_decisions():
    """
    Get the current final decisions and execution status.
    
    Returns:
        FinalDecisionsResponse: Current final decisions and execution status
    """
    try:
        decisions = execution_service.get_final_decisions()
        return FinalDecisionsResponse(**decisions)
        
    except Exception as e:
        logger.error(f"Error getting final decisions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/execution/execute", response_model=ExecuteResponse)
async def execute_signal(request: ExecuteRequest):
    """
    Execute a trade signal.
    
    Args:
        request: ExecuteRequest containing the signal ID
        
    Returns:
        ExecuteResponse: Execution result
    """
    try:
        result = execution_service.execute_signal(request.id)
        return ExecuteResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Invalid execution request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error executing signal: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 