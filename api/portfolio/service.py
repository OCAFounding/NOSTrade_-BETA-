from typing import Dict, Any, List, Optional
import logging
import numpy as np
from datetime import datetime, timedelta
from .config import get_portfolio_config

class PortfolioService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = get_portfolio_config()
        self.last_optimization_time = datetime.now()
        self.optimized_portfolio = []
        self.yield_routes = []
        
    def get_portfolio_status(self) -> Dict[str, Any]:
        """
        Get the current portfolio status including optimization and yield routing.
        
        Returns:
            Dict containing portfolio status, optimization results, and yield routes
        """
        self.logger.info("Getting portfolio status")
        
        # Check if we need to re-optimize
        if self._should_reoptimize():
            self._optimize_portfolio()
            
        # Update yield routes
        self._update_yield_routes()
        
        return {
            "portfolio": self.optimized_portfolio,
            "optimization": {
                "totalReturn": self._calculate_total_return(),
                "lastOptimized": self.last_optimization_time.isoformat(),
                "riskMetrics": self._calculate_risk_metrics()
            },
            "yieldRoutes": self.yield_routes
        }
    
    def _should_reoptimize(self) -> bool:
        """Check if portfolio needs re-optimization based on config settings."""
        time_since_last = datetime.now() - self.last_optimization_time
        return time_since_last.total_seconds() > self.config["optimization_interval"]
    
    def _optimize_portfolio(self) -> None:
        """Optimize the portfolio allocation based on current market conditions."""
        self.logger.info("Optimizing portfolio")
        
        # Get available assets and their metrics
        assets = self._get_available_assets()
        
        # Calculate optimal weights using Modern Portfolio Theory
        weights = self._calculate_optimal_weights(assets)
        
        # Update optimized portfolio
        self.optimized_portfolio = [
            {
                "name": asset["name"],
                "allocation": round(weight * 100, 2),
                "expectedReturn": asset["expected_return"],
                "risk": asset["risk"]
            }
            for asset, weight in zip(assets, weights)
        ]
        
        self.last_optimization_time = datetime.now()
        self.logger.info("Portfolio optimization completed")
    
    def _get_available_assets(self) -> List[Dict[str, Any]]:
        """Get list of available assets with their metrics."""
        # In a real implementation, this would fetch from a database or API
        return [
            {"name": "BTC", "expected_return": 0.15, "risk": 0.25},
            {"name": "ETH", "expected_return": 0.12, "risk": 0.20},
            {"name": "SOL", "expected_return": 0.18, "risk": 0.30},
            {"name": "AVAX", "expected_return": 0.16, "risk": 0.28},
            {"name": "DOT", "expected_return": 0.14, "risk": 0.22}
        ]
    
    def _calculate_optimal_weights(self, assets: List[Dict[str, Any]]) -> List[float]:
        """Calculate optimal portfolio weights using Modern Portfolio Theory."""
        returns = np.array([asset["expected_return"] for asset in assets])
        risks = np.array([asset["risk"] for asset in assets])
        
        # Simple equal risk contribution for demonstration
        # In a real implementation, this would use more sophisticated optimization
        weights = 1 / risks
        weights = weights / np.sum(weights)
        
        return weights.tolist()
    
    def _calculate_total_return(self) -> float:
        """Calculate the total expected return of the optimized portfolio."""
        if not self.optimized_portfolio:
            return 0.0
            
        total_return = sum(
            asset["allocation"] * asset["expectedReturn"] / 100
            for asset in self.optimized_portfolio
        )
        
        return round(total_return * 100, 2)
    
    def _calculate_risk_metrics(self) -> Dict[str, float]:
        """Calculate risk metrics for the optimized portfolio."""
        if not self.optimized_portfolio:
            return {"sharpe_ratio": 0.0, "volatility": 0.0}
            
        # Calculate portfolio volatility
        weights = np.array([asset["allocation"] / 100 for asset in self.optimized_portfolio])
        risks = np.array([asset["risk"] for asset in self.optimized_portfolio])
        portfolio_volatility = np.sqrt(np.sum((weights * risks) ** 2))
        
        # Calculate Sharpe ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        portfolio_return = self._calculate_total_return() / 100
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        
        return {
            "sharpe_ratio": round(sharpe_ratio, 2),
            "volatility": round(portfolio_volatility * 100, 2)
        }
    
    def _update_yield_routes(self) -> None:
        """Update yield routing data for available assets."""
        self.logger.info("Updating yield routes")
        
        # In a real implementation, this would fetch from yield sources
        self.yield_routes = [
            {"asset": "BTC", "yield": 4.5, "protocol": "Staking"},
            {"asset": "ETH", "yield": 5.2, "protocol": "Staking"},
            {"asset": "SOL", "yield": 6.8, "protocol": "Staking"},
            {"asset": "AVAX", "yield": 7.1, "protocol": "Staking"},
            {"asset": "DOT", "yield": 5.9, "protocol": "Staking"}
        ]
        
        self.logger.info("Yield routes updated") 