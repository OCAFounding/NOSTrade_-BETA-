from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
from pydantic import BaseModel
from .service import PortfolioService

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create router
router = APIRouter()

# Initialize service
portfolio_service = PortfolioService()

class PortfolioStatusResponse(BaseModel):
    """Response model for portfolio status endpoint"""
    portfolio: List[Dict[str, Any]]
    optimization: Dict[str, Any]
    yieldRoutes: List[Dict[str, Any]]

@router.get("/api/portfolio/status", response_model=PortfolioStatusResponse)
async def get_portfolio_status():
    """
    Get the current portfolio status including optimization and yield routing.
    
    Returns:
        PortfolioStatusResponse: Current portfolio status
    """
    try:
        status = portfolio_service.get_portfolio_status()
        return PortfolioStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Error getting portfolio status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/portfolio/optimize")
async def optimize_portfolio():
    """
    Force a portfolio optimization.
    
    Returns:
        Dict: Confirmation of optimization
    """
    try:
        portfolio_service._optimize_portfolio()
        return {
            "success": True,
            "message": "Portfolio optimization completed",
            "timestamp": portfolio_service.last_optimization_time.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/portfolio/yield-routes")
async def get_yield_routes():
    """
    Get current yield routing information.
    
    Returns:
        List[Dict]: Current yield routes
    """
    try:
        portfolio_service._update_yield_routes()
        return {
            "success": True,
            "yieldRoutes": portfolio_service.yield_routes
        }
        
    except Exception as e:
        logger.error(f"Error getting yield routes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 