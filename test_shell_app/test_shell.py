# from abc import ABC
import io
from unittest import TestCase
from unittest.mock import patch, Mock

from shell import Shell

TEST_VAL = "0x000000FF"


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_read_and_write(self):
        val = TEST_VAL
        self.shell.write(addr=10, val=val)
        self.assertEqual(val, self.shell.read(addr=10))

    def test_read_valid_input(self):
        mk = Mock(spec=Shell)
        mk.read.return_value = TEST_VAL

        self.assertEqual(TEST_VAL, mk.read(10))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_pos(self, mock_stdout):
        self.assertEqual("", self.shell.read(9999))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_neg(self, mock_stdout):
        self.assertEqual("", self.shell.read(-10))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")
