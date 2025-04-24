from agents.base_agent import BaseAgent

class ParentAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def delegate_tasks(self, tasks):
        for child, task in zip(self.children, tasks):
            child.receive_task(task)

    def aggregate_reports(self):
        return [child.report_status() for child in self.children] 