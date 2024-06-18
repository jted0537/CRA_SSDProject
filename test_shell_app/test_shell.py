# from abc import ABC
import io
from unittest import TestCase
from unittest.mock import patch, Mock

from shell import Shell

TEST_VAL = "0x000000FF"
INVALID_TEST_VAL = "0x000000ff"
TEST_ADDR = 10
LARGE_ADDR = 9999
NEG_ADDR = -10


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_read_and_write(self):
        self.shell.write(addr=TEST_ADDR, val=TEST_VAL)
        self.assertEqual(TEST_VAL, self.shell.read(addr=TEST_ADDR))

    def test_read_valid_input(self):
        mk = Mock(spec=Shell)
        mk.read.return_value = TEST_VAL

        self.assertEqual(TEST_VAL, mk.read(TEST_ADDR))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_pos(self, mock_stdout):
        self.assertEqual("", self.shell.read(LARGE_ADDR))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_neg(self, mock_stdout):
        self.assertEqual("", self.shell.read(NEG_ADDR))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_input_addr(self, mock_stdout):
        self.assertEqual("", self.shell.write(NEG_ADDR, TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_input_val(self, mock_stdout):
        self.assertEqual("", self.shell.write(TEST_ADDR, INVALID_TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), "INVALID PARAMETER\n")
