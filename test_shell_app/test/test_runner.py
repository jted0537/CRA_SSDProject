import io
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase
from unittest.mock import patch

from test_shell_app.Scripts.runner import Runner


class TestRunner(TestCase):
    def setUp(self):
        self.runner = Runner()

    def test_get_default_scenario_list(self):
        default_scenario_list = ["TestApp1", "TestApp2"]
        self.assertEqual(default_scenario_list, self.runner.get_scenario_list())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_exec_scenario_list(self, mock_stdout):
        self.assertTrue(self.runner.exec_scenario_list())
