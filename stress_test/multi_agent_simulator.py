import random
import time
import threading
import logging
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Remove global logging configuration as it's handled in run_stress_test.py
# logging.basicConfig(
#     filename='stress_test_results.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

class MultiAgentSimulator:
    """
    A simulator for testing multi-agent trading systems under stress conditions.
    """
    
    def __init__(
        self,
        agents: Optional[List[str]] = None,
        tasks: Optional[List[str]] = None,
        missing_data_prob: float = 0.2,
        failure_prob: float = 0.1,
        operations_per_agent: int = 100,
        min_delay: float = 0.05,
        max_delay: float = 0.15,
        output_dir: str = "stress_test_output"
    ):
        """
        Initialize the multi-agent simulator.
        
        Args:
            agents: List of agent names to simulate
            tasks: List of tasks to perform
            missing_data_prob: Probability of missing data (0.0-1.0)
            failure_prob: Probability of task failure (0.0-1.0)
            operations_per_agent: Number of operations each agent performs
            min_delay: Minimum delay between operations in seconds
            max_delay: Maximum delay between operations in seconds
            output_dir: Directory to store output files
        """
        self.agents = agents or ["StockAgent_A", "ForexAgent_B", "CryptoAgent_C", "ArbitrageAgent_D"]
        self.tasks = tasks or ["buy", "sell", "hedge", "rebalance"]
        self.missing_data_prob = missing_data_prob
        self.failure_prob = failure_prob
        self.operations_per_agent = operations_per_agent
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize memory log
        self.memory_log = []
        
        # Statistics
        self.stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "missing_data_events": 0,
            "start_time": None,
            "end_time": None,
            "agent_stats": {}
        }
        
        # Initialize agent statistics
        for agent in self.agents:
            self.stats["agent_stats"][agent] = {
                "total_operations": 0,
                "successful_operations": 0,
                "failed_operations": 0,
                "missing_data_events": 0
            }
    
    def simulate_agent_action(self, agent_name: str) -> None:
        """
        Simulate actions for a single agent.
        
        Args:
            agent_name: Name of the agent to simulate
        """
        for _ in range(self.operations_per_agent):
            task = random.choice(self.tasks)
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            # Update statistics
            self.stats["total_operations"] += 1
            self.stats["agent_stats"][agent_name]["total_operations"] += 1
            
            # Simulate missing data
            if random.random() < self.missing_data_prob:
                logging.warning(f"{agent_name} encountered missing data during {task} task.")
                self.stats["missing_data_events"] += 1
                self.stats["agent_stats"][agent_name]["missing_data_events"] += 1
                continue
            
            # Simulate failure
            if random.random() < self.failure_prob:
                logging.error(f"{agent_name} failed to complete {task} task.")
                self.stats["failed_operations"] += 1
                self.stats["agent_stats"][agent_name]["failed_operations"] += 1
                continue
            
            # Simulate success and memory push
            result = f"{agent_name} successfully completed {task}"
            self.memory_log.append({
                "agent": agent_name,
                "task": task,
                "timestamp": datetime.utcnow().isoformat()
            })
            logging.info(result)
            
            # Update success statistics
            self.stats["successful_operations"] += 1
            self.stats["agent_stats"][agent_name]["successful_operations"] += 1
    
    def run_simulation(self) -> Dict[str, Any]:
        """
        Run the multi-agent simulation.
        
        Returns:
            Dict[str, Any]: Simulation statistics
        """
        self.stats["start_time"] = datetime.utcnow().isoformat()
        
        # Launch threads for stress
        threads = []
        for agent in self.agents:
            t = threading.Thread(target=self.simulate_agent_action, args=(agent,))
            threads.append(t)
            t.start()
        
        # Join all threads
        for t in threads:
            t.join()
        
        self.stats["end_time"] = datetime.utcnow().isoformat()
        
        # Save memory snapshot
        memory_snapshot_path = os.path.join(self.output_dir, "agent_memory_snapshot.json")
        with open(memory_snapshot_path, "w") as f:
            json.dump(self.memory_log, f, indent=2)
        
        # Save statistics
        stats_path = os.path.join(self.output_dir, "simulation_statistics.json")
        with open(stats_path, "w") as f:
            json.dump(self.stats, f, indent=2)
        
        logging.info(f"Stress test completed. Logs and memory snapshot generated in {self.output_dir}.")
        return self.stats

def run_stress_test(
    agents: Optional[List[str]] = None,
    tasks: Optional[List[str]] = None,
    missing_data_prob: float = 0.2,
    failure_prob: float = 0.1,
    operations_per_agent: int = 100,
    min_delay: float = 0.05,
    max_delay: float = 0.15,
    output_dir: str = "stress_test_output"
) -> Dict[str, Any]:
    """
    Run a stress test with the specified parameters.
    
    Args:
        agents: List of agent names to simulate
        tasks: List of tasks to perform
        missing_data_prob: Probability of missing data (0.0-1.0)
        failure_prob: Probability of task failure (0.0-1.0)
        operations_per_agent: Number of operations each agent performs
        min_delay: Minimum delay between operations in seconds
        max_delay: Maximum delay between operations in seconds
        output_dir: Directory to store output files
        
    Returns:
        Dict[str, Any]: Simulation statistics
    """
    simulator = MultiAgentSimulator(
        agents=agents,
        tasks=tasks,
        missing_data_prob=missing_data_prob,
        failure_prob=failure_prob,
        operations_per_agent=operations_per_agent,
        min_delay=min_delay,
        max_delay=max_delay,
        output_dir=output_dir
    )
    
    return simulator.run_simulation()

# Remove the if __name__ == "__main__" block since it's redundant with run_stress_test.py
# if __name__ == "__main__":
#     # Run the stress test with default parameters
#     stats = run_stress_test()
#     
#     # Print summary
#     print("\nStress Test Summary:")
#     print(f"Total operations: {stats['total_operations']}")
#     print(f"Successful operations: {stats['successful_operations']}")
#     print(f"Failed operations: {stats['failed_operations']}")
#     print(f"Missing data events: {stats['missing_data_events']}")
#     print(f"Start time: {stats['start_time']}")
#     print(f"End time: {stats['end_time']}")
#     
#     print("\nAgent Statistics:")
#     for agent, agent_stats in stats["agent_stats"].items():
#         print(f"\n{agent}:")
#         print(f"  Total operations: {agent_stats['total_operations']}")
#         print(f"  Successful operations: {agent_stats['successful_operations']}")
#         print(f"  Failed operations: {agent_stats['failed_operations']}")
#         print(f"  Missing data events: {agent_stats['missing_data_events']}")
#     
#     print("\nStress test completed. Logs and memory snapshot generated.") 