# parent_agent.py
class ParentAgent:
    def __init__(self):
        self.strategy = "Diversified Risk-Controlled Growth"
    
    def assign_tasks(self, market_data):
        if market_data["volatility"] > 0.5:
            return "hedge", "reduce_exposure"
        return "trend_following", "momentum"

    def evaluate(self, child_reports):
        for report in child_reports:
            print(f"Child {report['name']} PnL: {report['profit']}")
