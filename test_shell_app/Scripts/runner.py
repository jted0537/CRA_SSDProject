class Runner:
    def __init__(self, file_name="run_list.lst"):
        self.scenario_list = self.get_scenario_list(file_name)

    def get_scenario_list(self, file_name="run_list.lst"):
        scenario_list = []
        with open(f"../{file_name}", "r") as file:
            for scenario in file:
                scenario_list.append(scenario.strip("\n"))

        return scenario_list
