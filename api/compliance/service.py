from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from .config import get_compliance_config
from .endpoints import ComplianceLog, add_compliance_log

class ComplianceService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = get_compliance_config()
        self.last_check_time = datetime.now()
        self.compliance_score = self.config["score_calculation"]["base_score"]
        
    def check_compliance(self, trading_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a comprehensive compliance check on the trading state.
        
        Args:
            trading_state: Current trading state including positions, P&L, etc.
            
        Returns:
            Dict containing compliance check results
        """
        self.logger.info("Starting compliance check")
        results = {
            "timestamp": datetime.now().isoformat(),
            "score": self.compliance_score,
            "violations": [],
            "warnings": [],
            "checks_performed": []
        }
        
        # Check drawdown
        self._check_drawdown(trading_state, results)
        
        # Check position sizes
        self._check_position_sizes(trading_state, results)
        
        # Check daily trade count
        self._check_daily_trades(trading_state, results)
        
        # Update compliance score
        self._update_compliance_score(results)
        
        # Log the check
        self._log_compliance_check(results)
        
        return results
    
    def _check_drawdown(self, trading_state: Dict[str, Any], results: Dict[str, Any]) -> None:
        """Check if current drawdown exceeds limits."""
        current_drawdown = trading_state.get("current_drawdown", 0)
        max_allowed_drawdown = trading_state.get("max_allowed_drawdown", 0.1)  # 10%
        
        results["checks_performed"].append("drawdown")
        
        if current_drawdown > max_allowed_drawdown:
            violation = {
                "type": "drawdown",
                "current": current_drawdown,
                "limit": max_allowed_drawdown,
                "message": f"Drawdown {current_drawdown:.2%} exceeds limit of {max_allowed_drawdown:.2%}"
            }
            results["violations"].append(violation)
            add_compliance_log(
                message=violation["message"],
                level="violation",
                category="risk",
                details=violation
            )
    
    def _check_position_sizes(self, trading_state: Dict[str, Any], results: Dict[str, Any]) -> None:
        """Check if position sizes are within limits."""
        positions = trading_state.get("positions", {})
        max_position_size = trading_state.get("max_position_size", 1.0)
        
        results["checks_performed"].append("position_sizes")
        
        for symbol, position in positions.items():
            size = abs(position.get("size", 0))
            if size > max_position_size:
                violation = {
                    "type": "position_size",
                    "symbol": symbol,
                    "current": size,
                    "limit": max_position_size,
                    "message": f"Position size {size} for {symbol} exceeds limit of {max_position_size}"
                }
                results["violations"].append(violation)
                add_compliance_log(
                    message=violation["message"],
                    level="violation",
                    category="position",
                    details=violation
                )
    
    def _check_daily_trades(self, trading_state: Dict[str, Any], results: Dict[str, Any]) -> None:
        """Check if daily trade count is within limits."""
        daily_trades = trading_state.get("daily_trades", 0)
        max_daily_trades = trading_state.get("max_daily_trades", 50)
        
        results["checks_performed"].append("daily_trades")
        
        if daily_trades > max_daily_trades:
            violation = {
                "type": "daily_trades",
                "current": daily_trades,
                "limit": max_daily_trades,
                "message": f"Daily trade count {daily_trades} exceeds limit of {max_daily_trades}"
            }
            results["violations"].append(violation)
            add_compliance_log(
                message=violation["message"],
                level="violation",
                category="trade",
                details=violation
            )
    
    def _update_compliance_score(self, results: Dict[str, Any]) -> None:
        """Update the compliance score based on check results."""
        score = self.config["score_calculation"]["base_score"]
        
        # Apply penalties
        for violation in results["violations"]:
            score -= self.config["score_calculation"]["violation_penalty"]
        
        for warning in results["warnings"]:
            score -= self.config["score_calculation"]["warning_penalty"]
        
        # Ensure score stays within bounds
        self.compliance_score = max(0, min(100, score))
        results["score"] = self.compliance_score
    
    def _log_compliance_check(self, results: Dict[str, Any]) -> None:
        """Log the compliance check results."""
        if results["violations"]:
            self.logger.warning(f"Compliance check found {len(results['violations'])} violations")
        elif results["warnings"]:
            self.logger.info(f"Compliance check found {len(results['warnings'])} warnings")
        else:
            self.logger.info("Compliance check passed with no issues")
        
        add_compliance_log(
            message=f"Compliance check completed with score {results['score']}",
            level="info" if not results["violations"] else "warning",
            category="general",
            details=results
        )
    
    def get_compliance_score(self) -> float:
        """Get the current compliance score."""
        return self.compliance_score
    
    def reset_compliance_score(self) -> None:
        """Reset the compliance score to the base value."""
        self.compliance_score = self.config["score_calculation"]["base_score"]
        self.logger.info("Compliance score reset to base value") 