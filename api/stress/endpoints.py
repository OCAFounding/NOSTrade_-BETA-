from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import json
import os
from datetime import datetime

from stress_test.multi_agent_simulator import MultiAgentSimulator, run_stress_test
from stress_test.visualization import generate_visualization_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Global variables to track stress test state
stress_test_running = False
stress_test_simulator = None
stress_test_output_dir = "stress_test_output"

class StressTestConfig(BaseModel):
    """Configuration for stress test."""
    failSim: bool = True
    missingData: bool = True
    agents: Optional[List[str]] = None
    tasks: Optional[List[str]] = None
    operations_per_agent: int = 100
    min_delay: float = 0.05
    max_delay: float = 0.15

class StressTestResponse(BaseModel):
    """Response for stress test operations."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class LogSummaryResponse(BaseModel):
    """Response for log summary."""
    summary: str
    timestamp: str

@router.post("/api/stress/start", response_model=StressTestResponse)
async def start_stress_test(config: StressTestConfig, background_tasks: BackgroundTasks):
    """
    Start a stress test with the given configuration.
    
    Args:
        config: Stress test configuration
        background_tasks: FastAPI background tasks
        
    Returns:
        StressTestResponse: Response indicating success or failure
    """
    global stress_test_running, stress_test_simulator
    
    if stress_test_running:
        raise HTTPException(status_code=400, detail="Stress test is already running")
    
    try:
        # Create output directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"{stress_test_output_dir}_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Configure simulator
        stress_test_simulator = MultiAgentSimulator(
            agents=config.agents,
            tasks=config.tasks,
            missing_data_prob=0.2 if config.missingData else 0.0,
            failure_prob=0.1 if config.failSim else 0.0,
            operations_per_agent=config.operations_per_agent,
            min_delay=config.min_delay,
            max_delay=config.max_delay,
            output_dir=output_dir
        )
        
        # Run simulation in background
        stress_test_running = True
        background_tasks.add_task(run_stress_test_in_background, output_dir)
        
        return StressTestResponse(
            success=True,
            message="Stress test started successfully",
            data={"output_dir": output_dir}
        )
    
    except Exception as e:
        logger.error(f"Failed to start stress test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start stress test: {str(e)}")

@router.post("/api/stress/stop", response_model=StressTestResponse)
async def stop_stress_test():
    """
    Stop the currently running stress test.
    
    Returns:
        StressTestResponse: Response indicating success or failure
    """
    global stress_test_running, stress_test_simulator
    
    if not stress_test_running:
        raise HTTPException(status_code=400, detail="No stress test is currently running")
    
    try:
        # Stop the simulator
        stress_test_running = False
        stress_test_simulator = None
        
        return StressTestResponse(
            success=True,
            message="Stress test stopped successfully"
        )
    
    except Exception as e:
        logger.error(f"Failed to stop stress test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to stop stress test: {str(e)}")

@router.get("/api/stress/log-summary", response_model=LogSummaryResponse)
async def get_log_summary():
    """
    Get a summary of the most recent stress test log.
    
    Returns:
        LogSummaryResponse: Log summary and timestamp
    """
    try:
        # Find the most recent output directory
        output_dirs = [d for d in os.listdir() if d.startswith(stress_test_output_dir)]
        if not output_dirs:
            return LogSummaryResponse(
                summary="No stress test logs found",
                timestamp=datetime.now().isoformat()
            )
        
        latest_dir = max(output_dirs)
        
        # Load statistics
        stats_path = os.path.join(latest_dir, "simulation_statistics.json")
        if not os.path.exists(stats_path):
            return LogSummaryResponse(
                summary="No statistics found for the latest stress test",
                timestamp=datetime.now().isoformat()
            )
        
        with open(stats_path, "r") as f:
            stats = json.load(f)
        
        # Generate summary
        total_ops = stats["total_operations"]
        success_rate = (stats["successful_operations"] / total_ops) * 100 if total_ops > 0 else 0
        failure_rate = (stats["failed_operations"] / total_ops) * 100 if total_ops > 0 else 0
        missing_rate = (stats["missing_data_events"] / total_ops) * 100 if total_ops > 0 else 0
        
        # Calculate duration
        start_time = datetime.fromisoformat(stats["start_time"])
        end_time = datetime.fromisoformat(stats["end_time"])
        duration = end_time - start_time
        
        summary = f"""
Stress Test Summary
------------------
Total Operations: {total_ops}
Successful Operations: {stats["successful_operations"]} ({success_rate:.1f}%)
Failed Operations: {stats["failed_operations"]} ({failure_rate:.1f}%)
Missing Data Events: {stats["missing_data_events"]} ({missing_rate:.1f}%)
Duration: {duration.total_seconds():.2f} seconds

Agent Statistics:
"""
        
        for agent, agent_stats in stats["agent_stats"].items():
            agent_total = agent_stats["total_operations"]
            agent_success = agent_stats["successful_operations"]
            agent_failed = agent_stats["failed_operations"]
            agent_missing = agent_stats["missing_data_events"]
            agent_success_rate = (agent_success / agent_total) * 100 if agent_total > 0 else 0
            
            summary += f"""
{agent}:
  Total Operations: {agent_total}
  Successful: {agent_success} ({agent_success_rate:.1f}%)
  Failed: {agent_failed}
  Missing Data: {agent_missing}
"""
        
        return LogSummaryResponse(
            summary=summary,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Failed to get log summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get log summary: {str(e)}")

async def run_stress_test_in_background(output_dir: str):
    """
    Run the stress test in the background.
    
    Args:
        output_dir: Directory to store output files
    """
    global stress_test_running
    
    try:
        # Run the stress test
        stats = run_stress_test(output_dir=output_dir)
        
        # Generate visualization report
        generate_visualization_report(output_dir)
        
        logger.info(f"Stress test completed. Results saved to {output_dir}")
    
    except Exception as e:
        logger.error(f"Error in background stress test: {str(e)}")
    
    finally:
        stress_test_running = False 