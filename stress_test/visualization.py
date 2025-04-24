import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime

def load_simulation_data(output_dir: str = "stress_test_output") -> Dict[str, Any]:
    """
    Load simulation data from the output directory.
    
    Args:
        output_dir: Directory containing simulation output files
        
    Returns:
        Dict[str, Any]: Simulation data
    """
    stats_path = os.path.join(output_dir, "simulation_statistics.json")
    memory_path = os.path.join(output_dir, "agent_memory_snapshot.json")
    
    if not os.path.exists(stats_path):
        raise FileNotFoundError(f"Statistics file not found: {stats_path}")
    
    with open(stats_path, "r") as f:
        stats = json.load(f)
    
    memory_data = []
    if os.path.exists(memory_path):
        with open(memory_path, "r") as f:
            memory_data = json.load(f)
    
    return {
        "stats": stats,
        "memory": memory_data
    }

def _ensure_output_dir(output_dir: str) -> None:
    """
    Ensure the output directory exists.
    
    Args:
        output_dir: Directory to check/create
    """
    os.makedirs(output_dir, exist_ok=True)

def plot_operation_results(stats: Dict[str, Any], output_dir: str = "stress_test_output") -> None:
    """
    Plot operation results as a pie chart.
    
    Args:
        stats: Simulation statistics
        output_dir: Directory to save the plot
    """
    labels = ["Successful", "Failed", "Missing Data"]
    sizes = [
        stats["successful_operations"],
        stats["failed_operations"],
        stats["missing_data_events"]
    ]
    colors = ["#4CAF50", "#F44336", "#FFC107"]
    
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title("Operation Results")
    
    # Save the plot
    _ensure_output_dir(output_dir)
    plt.savefig(os.path.join(output_dir, "operation_results.png"))
    plt.close()

def plot_agent_performance(stats: Dict[str, Any], output_dir: str = "stress_test_output") -> None:
    """
    Plot agent performance as a bar chart.
    
    Args:
        stats: Simulation statistics
        output_dir: Directory to save the plot
    """
    agents = list(stats["agent_stats"].keys())
    successful = [stats["agent_stats"][agent]["successful_operations"] for agent in agents]
    failed = [stats["agent_stats"][agent]["failed_operations"] for agent in agents]
    missing = [stats["agent_stats"][agent]["missing_data_events"] for agent in agents]
    
    x = range(len(agents))
    width = 0.25
    
    plt.figure(figsize=(12, 8))
    plt.bar([i - width for i in x], successful, width, label="Successful", color="#4CAF50")
    plt.bar(x, failed, width, label="Failed", color="#F44336")
    plt.bar([i + width for i in x], missing, width, label="Missing Data", color="#FFC107")
    
    plt.xlabel("Agents")
    plt.ylabel("Number of Operations")
    plt.title("Agent Performance")
    plt.xticks(x, agents, rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    _ensure_output_dir(output_dir)
    plt.savefig(os.path.join(output_dir, "agent_performance.png"))
    plt.close()

def plot_task_distribution(memory_data: List[Dict[str, Any]], output_dir: str = "stress_test_output") -> None:
    """
    Plot task distribution as a bar chart.
    
    Args:
        memory_data: Memory snapshot data
        output_dir: Directory to save the plot
    """
    if not memory_data:
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(memory_data)
    
    # Count tasks
    task_counts = df["task"].value_counts()
    
    plt.figure(figsize=(10, 8))
    task_counts.plot(kind="bar", color="#2196F3")
    plt.xlabel("Task")
    plt.ylabel("Count")
    plt.title("Task Distribution")
    plt.tight_layout()
    
    # Save the plot
    _ensure_output_dir(output_dir)
    plt.savefig(os.path.join(output_dir, "task_distribution.png"))
    plt.close()

def plot_agent_task_heatmap(memory_data: List[Dict[str, Any]], output_dir: str = "stress_test_output") -> None:
    """
    Plot agent-task heatmap.
    
    Args:
        memory_data: Memory snapshot data
        output_dir: Directory to save the plot
    """
    if not memory_data:
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(memory_data)
    
    # Create a pivot table
    pivot = pd.pivot_table(
        df, 
        values="timestamp", 
        index="agent", 
        columns="task", 
        aggfunc="count",
        fill_value=0
    )
    
    plt.figure(figsize=(12, 8))
    plt.imshow(pivot, cmap="YlOrRd", aspect="auto")
    plt.colorbar(label="Count")
    plt.xlabel("Task")
    plt.ylabel("Agent")
    plt.title("Agent-Task Heatmap")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.tight_layout()
    
    # Save the plot
    _ensure_output_dir(output_dir)
    plt.savefig(os.path.join(output_dir, "agent_task_heatmap.png"))
    plt.close()

def plot_timeline(memory_data: List[Dict[str, Any]], output_dir: str = "stress_test_output") -> None:
    """
    Plot operation timeline.
    
    Args:
        memory_data: Memory snapshot data
        output_dir: Directory to save the plot
    """
    if not memory_data:
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(memory_data)
    
    # Convert timestamps to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Sort by timestamp
    df = df.sort_values("timestamp")
    
    # Create a scatter plot
    plt.figure(figsize=(15, 8))
    
    # Plot each agent with a different color
    agents = df["agent"].unique()
    colors = plt.cm.tab10.colors
    
    for i, agent in enumerate(agents):
        agent_data = df[df["agent"] == agent]
        plt.scatter(
            agent_data["timestamp"], 
            [i] * len(agent_data), 
            label=agent,
            color=colors[i % len(colors)],
            alpha=0.7
        )
    
    plt.xlabel("Time")
    plt.ylabel("Agent")
    plt.title("Operation Timeline")
    plt.yticks(range(len(agents)), agents)
    plt.grid(True, axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    
    # Save the plot
    _ensure_output_dir(output_dir)
    plt.savefig(os.path.join(output_dir, "operation_timeline.png"))
    plt.close()

def generate_visualization_report(output_dir: str = "stress_test_output") -> None:
    """
    Generate a comprehensive visualization report.
    
    Args:
        output_dir: Directory containing simulation output files
    """
    # Load data
    data = load_simulation_data(output_dir)
    stats = data["stats"]
    memory_data = data["memory"]
    
    # Generate plots
    plot_operation_results(stats, output_dir)
    plot_agent_performance(stats, output_dir)
    
    if memory_data:
        plot_task_distribution(memory_data, output_dir)
        plot_agent_task_heatmap(memory_data, output_dir)
        plot_timeline(memory_data, output_dir)
    
    # Generate HTML report
    generate_html_report(stats, memory_data, output_dir)

def generate_html_report(stats: Dict[str, Any], memory_data: List[Dict[str, Any]], output_dir: str) -> None:
    """
    Generate an HTML report with visualizations and statistics.
    
    Args:
        stats: Simulation statistics
        memory_data: Memory snapshot data
        output_dir: Directory to save the report
    """
    # Calculate statistics
    total_ops = stats["total_operations"]
    success_rate = (stats["successful_operations"] / total_ops) * 100 if total_ops > 0 else 0
    failure_rate = (stats["failed_operations"] / total_ops) * 100 if total_ops > 0 else 0
    missing_rate = (stats["missing_data_events"] / total_ops) * 100 if total_ops > 0 else 0
    
    # Calculate duration
    start_time = datetime.fromisoformat(stats["start_time"])
    end_time = datetime.fromisoformat(stats["end_time"])
    duration = end_time - start_time
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NOS Trade Stress Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .stats-container {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ 
                background-color: #f5f5f5; 
                border-radius: 5px; 
                padding: 15px; 
                flex: 1; 
                min-width: 200px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .stat-value {{ font-size: 24px; font-weight: bold; color: #2196F3; }}
            .visualization {{ margin-bottom: 30px; }}
            .visualization img {{ max-width: 100%; border: 1px solid #ddd; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
            .success {{ color: #4CAF50; }}
            .failure {{ color: #F44336; }}
            .warning {{ color: #FFC107; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>NOS Trade Stress Test Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Summary Statistics</h2>
            <div class="stats-container">
                <div class="stat-card">
                    <h3>Total Operations</h3>
                    <div class="stat-value">{total_ops}</div>
                </div>
                <div class="stat-card">
                    <h3>Success Rate</h3>
                    <div class="stat-value success">{success_rate:.1f}%</div>
                </div>
                <div class="stat-card">
                    <h3>Failure Rate</h3>
                    <div class="stat-value failure">{failure_rate:.1f}%</div>
                </div>
                <div class="stat-card">
                    <h3>Missing Data Rate</h3>
                    <div class="stat-value warning">{missing_rate:.1f}%</div>
                </div>
                <div class="stat-card">
                    <h3>Duration</h3>
                    <div class="stat-value">{duration.total_seconds():.2f} seconds</div>
                </div>
            </div>
            
            <h2>Visualizations</h2>
            
            <div class="visualization">
                <h3>Operation Results</h3>
                <img src="operation_results.png" alt="Operation Results">
            </div>
            
            <div class="visualization">
                <h3>Agent Performance</h3>
                <img src="agent_performance.png" alt="Agent Performance">
            </div>
    """
    
    # Add memory visualizations if available
    if memory_data:
        html_content += """
            <div class="visualization">
                <h3>Task Distribution</h3>
                <img src="task_distribution.png" alt="Task Distribution">
            </div>
            
            <div class="visualization">
                <h3>Agent-Task Heatmap</h3>
                <img src="agent_task_heatmap.png" alt="Agent-Task Heatmap">
            </div>
            
            <div class="visualization">
                <h3>Operation Timeline</h3>
                <img src="operation_timeline.png" alt="Operation Timeline">
            </div>
        """
    
    # Add agent statistics table
    html_content += """
            <h2>Agent Statistics</h2>
            <table>
                <tr>
                    <th>Agent</th>
                    <th>Total Operations</th>
                    <th>Successful</th>
                    <th>Failed</th>
                    <th>Missing Data</th>
                    <th>Success Rate</th>
                </tr>
    """
    
    for agent, agent_stats in stats["agent_stats"].items():
        agent_total = agent_stats["total_operations"]
        agent_success = agent_stats["successful_operations"]
        agent_failed = agent_stats["failed_operations"]
        agent_missing = agent_stats["missing_data_events"]
        agent_success_rate = (agent_success / agent_total) * 100 if agent_total > 0 else 0
        
        html_content += f"""
                <tr>
                    <td>{agent}</td>
                    <td>{agent_total}</td>
                    <td class="success">{agent_success}</td>
                    <td class="failure">{agent_failed}</td>
                    <td class="warning">{agent_missing}</td>
                    <td>{agent_success_rate:.1f}%</td>
                </tr>
        """
    
    html_content += """
            </table>
        </div>
    </body>
    </html>
    """
    
    # Save the HTML report
    _ensure_output_dir(output_dir)
    report_path = os.path.join(output_dir, "stress_test_report.html")
    with open(report_path, "w") as f:
        f.write(html_content)
    
    print(f"HTML report generated: {report_path}") 