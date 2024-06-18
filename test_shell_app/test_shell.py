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

    @patch.object(Shell, "write")
    def test_full_write(self, mk):
        def write(addr, val):
            self.shell._lbas[addr] = val

        mk.side_effect = write

        self.shell.full_write(0x12345678)
        self.assertEqual(self.shell._lbas, [0x12345678] * 100)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(Shell, "read")
    def test_full_read(self, mk, mk_stdout):
        def read(addr):
            print(self.shell._lbas[addr])

        mk.side_effect = read

        self.shell.full_read()
        self.assertIn("0\n0\n0\n0", mk_stdout.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_full_read_without_mock(self, mock_stdout):
        self.shell.full_read()
        output = mock_stdout.getvalue()
        self.assertEqual(output.count("EXCEPTION OCCUR stderr"), 100)
