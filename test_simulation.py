from agents.parent_agent import ParentAgent
from agents.child_agent import ChildAgent
from strategies.momentum_strategy import momentum_strategy

if __name__ == "__main__":
    parent = ParentAgent("MetaTrader AI")

    # Example child agents with dummy strategies
    child1 = ChildAgent("MomentumBot", momentum_strategy)
    child2 = ChildAgent("ArbitrageBot", lambda task: f"[Arbitrage] Checked {task['symbol']} across exchanges.")

    parent.add_child(child1)
    parent.add_child(child2)

    tasks = [
        {"symbol": "BTC/USDT", "type": "momentum"},
        {"symbol": "ETH/USDT", "type": "arbitrage"}
    ]

    parent.delegate_tasks(tasks)
    reports = parent.aggregate_reports()
    for report in reports:
        print(report) 