class BaseAgent:
    def __init__(self, name):
        self.name = name

    def receive_task(self, task):
        raise NotImplementedError("Each agent must implement this method.")

    def report_status(self):
        return f"{self.name} reporting in." 