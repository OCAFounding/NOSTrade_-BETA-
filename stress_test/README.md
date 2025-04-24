# NOS Trade Multi-Agent Stress Test Module

This module provides a comprehensive stress testing framework for the NOS Trade multi-agent trading system. It simulates multiple trading agents operating concurrently under various stress conditions to evaluate system performance, reliability, and error handling.

## Features

- **Multi-agent Simulation**: Simulates multiple trading agents operating concurrently
- **Configurable Parameters**: Customize agents, tasks, failure rates, and timing
- **Comprehensive Logging**: Detailed logging of all operations, failures, and events
- **Statistical Analysis**: Generates detailed statistics on system performance
- **Memory Snapshot**: Creates a persistent log of successful operations
- **Thread-based Concurrency**: Uses Python threading for realistic concurrent operation

## Usage

### Basic Usage

```python
from stress_test.multi_agent_simulator import run_stress_test

# Run with default parameters
stats = run_stress_test()
```

### Customized Stress Test

```python
from stress_test.multi_agent_simulator import run_stress_test

# Customize the stress test
stats = run_stress_test(
    agents=["CustomAgent_1", "CustomAgent_2", "CustomAgent_3"],
    tasks=["buy", "sell", "analyze"],
    missing_data_prob=0.3,  # 30% chance of missing data
    failure_prob=0.15,      # 15% chance of failure
    operations_per_agent=200,  # Each agent performs 200 operations
    min_delay=0.01,         # Minimum 10ms delay
    max_delay=0.05,         # Maximum 50ms delay
    output_dir="custom_stress_test"
)
```

### Using the MultiAgentSimulator Class Directly

```python
from stress_test.multi_agent_simulator import MultiAgentSimulator

# Create a simulator instance
simulator = MultiAgentSimulator(
    agents=["Agent_A", "Agent_B"],
    tasks=["buy", "sell"],
    missing_data_prob=0.2,
    failure_prob=0.1
)

# Run the simulation
stats = simulator.run_simulation()

# Access the results
print(f"Total operations: {stats['total_operations']}")
print(f"Successful operations: {stats['successful_operations']}")
print(f"Failed operations: {stats['failed_operations']}")
```

## Output Files

The stress test generates the following output files:

1. **stress_test_results.log**: Detailed log of all operations, including:
   - Successful operations
   - Failed operations
   - Missing data events
   - Timestamps for all events

2. **agent_memory_snapshot.json**: JSON file containing a record of all successful operations:
   - Agent name
   - Task performed
   - Timestamp

3. **simulation_statistics.json**: JSON file with comprehensive statistics:
   - Total operations
   - Successful operations
   - Failed operations
   - Missing data events
   - Start and end times
   - Per-agent statistics

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `agents` | List of agent names to simulate | `["StockAgent_A", "ForexAgent_B", "CryptoAgent_C", "ArbitrageAgent_D"]` |
| `tasks` | List of tasks to perform | `["buy", "sell", "hedge", "rebalance"]` |
| `missing_data_prob` | Probability of missing data (0.0-1.0) | `0.2` |
| `failure_prob` | Probability of task failure (0.0-1.0) | `0.1` |
| `operations_per_agent` | Number of operations each agent performs | `100` |
| `min_delay` | Minimum delay between operations in seconds | `0.05` |
| `max_delay` | Maximum delay between operations in seconds | `0.15` |
| `output_dir` | Directory to store output files | `"stress_test_output"` |

## Integration with NOS Trade

This stress test module is designed to be integrated with the NOS Trade system to evaluate:

1. **System Stability**: How the system handles concurrent operations from multiple agents
2. **Error Handling**: How the system responds to missing data and failures
3. **Performance**: How the system performs under load
4. **Memory Management**: How the system manages memory during extended operation

## Future Enhancements

- Add support for simulating network latency and bandwidth constraints
- Implement more realistic market data simulation
- Add visualization tools for stress test results
- Integrate with CI/CD pipelines for automated testing 