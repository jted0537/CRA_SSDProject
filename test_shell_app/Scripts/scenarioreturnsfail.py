import os, sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from Utils.script import Script
from shell import Shell


class ScenarioReturnsFail(Script):
    def __init__(self):
        super().__init__()
        self.shell = Shell()

    def run(self):
        print("Scenario Fail")
        return False
