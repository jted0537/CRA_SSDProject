# from abc import ABC
import io
from unittest import TestCase
from unittest.mock import patch, Mock

from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_print(self):
        pass

    # @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_valid_input(self):
        mk = Mock(spec=Shell)
        mk.read.return_value = 3

        self.assertEqual(3, mk.read(10))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_pos(self, mock_stdout):
        self.assertEqual(-1, self.shell.read(9999))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_neg(self, mock_stdout):
        self.assertEqual(-1, self.shell.read(-10))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")
