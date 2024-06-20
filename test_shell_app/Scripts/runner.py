import sys
import io
import importlib


class Runner:
    def __init__(self, file_name="run_list.lst"):
        self.scenario_list = self.get_scenario_list(file_name)

    def get_scenario_list(self, file_name="run_list.lst"):
        scenario_list = []
        with open(f"../{file_name}", "r") as file:
            for scenario in file:
                scenario_list.append(scenario.strip("\n"))

        return scenario_list

    def exec_scenario_list(self):
        for scenario in self.scenario_list:
            print(f"{scenario}  ---  Run...", end="")
            captured_output = io.StringIO()
            sys.stdout = captured_output

            val1 = eval(f"importlib.import_module('{scenario.lower()}')")
            val2 = eval(f"val1.{scenario}()")
            rst = val2.run()

            sys.stdout = sys.__stdout__
            if rst:
                print("Pass")
            else:
                print("FAIL!")
                break
