import contextlib
import os
import sys
import io
import importlib


CURR_DIR_NAME = os.path.dirname(os.path.abspath(__file__))
CURR_FOLDER_NAME = os.path.basename(CURR_DIR_NAME)

SCRIPTS_FOLDER_NAME = "Scripts"


class ScenarioFactory:
    @staticmethod
    def create_scenario(scenario_name):
        module = importlib.import_module(
            f"{SCRIPTS_FOLDER_NAME}.{scenario_name.lower()}"
        )
        scenario_class = getattr(module, scenario_name)
        return scenario_class()


class Runner:
    def __init__(self, file_name="run_list.lst"):
        self.scenario_list = self.get_scenario_list(file_name)

    def set_scenario_list(self, file_name):
        self.scenario_list = self.get_scenario_list(file_name)

    def get_scenario_list(self, file_name="run_list.lst"):
        scenario_list = []
        with open(f"{CURR_DIR_NAME}//{file_name}", "r") as file:
            for scenario in file:
                scenario_list.append(scenario.strip("\n"))

        return scenario_list

    def exec_scenario_list(self):
        for scenario_name in self.scenario_list:
            print(f"{scenario_name}  ---  Run...", end="", flush=True)

            scenario = ScenarioFactory.create_scenario(scenario_name)
            with contextlib.redirect_stdout(io.StringIO()) as f:
                rst = scenario.run()

            if not rst:
                print(" FAIL!")
                return False
            print(" Pass")
        return True


def find_lst_files(directory):
    lst_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".lst"):
                lst_files.append(file)
    return lst_files


def main(argv):
    lst_files = find_lst_files(CURR_DIR_NAME)
    if argv[1] in lst_files:
        runner = Runner(argv[1])
        runner.exec_scenario_list()
    else:
        print("다른 파일 명을 입력하세요.")


if __name__ == "__main__":
    main(sys.argv)
