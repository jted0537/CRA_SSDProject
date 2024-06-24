from Utils.script import Script
from shell import Shell


class ScenarioReturnsFail(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        print("Scenario Fail")
        return False
