from agents.base_agent import BaseAgent

class ChildAgent(BaseAgent):
    def __init__(self, name, strategy_fn):
        super().__init__(name)
        self.strategy_fn = strategy_fn

    def receive_task(self, task):
        print(f"{self.name} executing task: {task}")
        return self.strategy_fn(task) 