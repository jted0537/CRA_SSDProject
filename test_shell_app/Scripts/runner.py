import os
import sys
import io
import importlib

CURR_FOLDER_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


class ScenarioFactory:
    @staticmethod
    def create_scenario(scenario_name):
        if os.path.basename(os.path.dirname(os.getcwd())) == CURR_FOLDER_NAME:
            module = importlib.import_module(scenario_name.lower())
        else:
            module = importlib.import_module(
                f"{CURR_FOLDER_NAME}.{scenario_name.lower()}"
            )
        scenario_class = getattr(module, scenario_name)
        return scenario_class()


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
        for scenario_name in self.scenario_list:
            print(f"{scenario_name}  ---  Run...", end="")
            captured_output = io.StringIO()
            sys.stdout = captured_output

            scenario = ScenarioFactory.create_scenario(scenario_name)

            try:
                rst = scenario.run()
            except Exception as e:
                print("Exception", e)
                break
            finally:
                sys.stdout = sys.__stdout__

            if rst:
                print("Pass")
            else:
                print("FAIL!")
                return False
        return True


if __name__ == "__main__":
    runner = Runner()
    runner.exec_scenario_list()
