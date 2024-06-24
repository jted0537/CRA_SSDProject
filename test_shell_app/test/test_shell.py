import io
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase
from unittest.mock import patch

from test_shell_app.shell import Shell
from test_shell_app.Utils.message_manager import InvalidArgumentMessageManager

INVALID_PARAMETER_TEXT = InvalidArgumentMessageManager().message
EXCEPTION_OCCUR_TEXT = "EXCEPTION OCCUR"
INITIAL_VAL = "0x00000000"
VALID_TEST_VAL = "0x000000FF"
VALID_TEST_ADDR = 10
VALID_TEST_ADDR_WITHOUT_WRITE = 30


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()
        self.orig_stdout = sys.stdout

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_and_write(self, mock_stdout):
        self.shell.write(addr=VALID_TEST_ADDR, val=VALID_TEST_VAL)
        read_value = self.shell.read(addr=VALID_TEST_ADDR)
        self.assertNotIn(EXCEPTION_OCCUR_TEXT, mock_stdout.getvalue())
        self.assertEqual(VALID_TEST_VAL, read_value)

    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_read_valid_addr_without_write(self, mock_stdout):
    #     self.shell.read(addr=VALID_TEST_ADDR)
    #     self.assertNotIn(EXCEPTION_OCCUR_TEXT, mock_stdout.getvalue())
    #     self.assertEqual(
    #         INITIAL_VAL, self.shell.read(addr=VALID_TEST_ADDR_WITHOUT_WRITE)
    #     )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_parameter(self, mock_stdout):
        test_cases = [
            (-10, INVALID_PARAMETER_TEXT),
            (9999, INVALID_PARAMETER_TEXT),
        ]
        for addr, expected_output in test_cases:
            with self.subTest(f"ssd R {addr}"):
                self.assertIsNone(self.shell.read(addr))
                self.assertEqual(mock_stdout.getvalue(), expected_output)
                sys.stdout = self.orig_stdout

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_parameter(self, mock_stdout):
        test_cases = [
            (10, "0x000FF", INVALID_PARAMETER_TEXT),
            (10, "00000000FF", INVALID_PARAMETER_TEXT),
            (10, "0x0000ZZFF", INVALID_PARAMETER_TEXT),
            (9999, "0x000000FF", INVALID_PARAMETER_TEXT),
            (-10, "0x000000FF", INVALID_PARAMETER_TEXT),
        ]
        for addr, val, expected_output in test_cases:
            with self.subTest(f"ssd W {addr} {val}"):
                self.assertIsNone(self.shell.write(addr, val))
                self.assertEqual(mock_stdout.getvalue(), expected_output)
                sys.stdout = self.orig_stdout

    @patch.object(Shell, "write")
    def test_full_write(self, mk):
        self.shell._lbas = [0] * self.shell.MAX_ADDR

        def write(addr, val):
            self.shell._lbas[addr] = val

        mk.side_effect = write

        self.shell.full_write(VALID_TEST_VAL)
        self.assertEqual(self.shell._lbas, [VALID_TEST_VAL] * self.shell.MAX_ADDR)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(Shell, "read")
    def test_full_read(self, mk, mock_stdout):
        self.shell._lbas = [0] * self.shell.MAX_ADDR

        def read(addr):
            print(self.shell._lbas[addr])

        mk.side_effect = read

        self.shell.full_read()
        output = mock_stdout.getvalue()
        self.assertEqual(output.count("\n"), self.shell.MAX_ADDR)

    def test_full_write_with_write(self):
        output = self.shell.full_write(VALID_TEST_VAL)
        self.assertEqual(output, self.shell.SUCCESS)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_full_read_with_read(self, mock_stdout):
        self.shell.full_read()
        output = mock_stdout.getvalue()
        self.assertEqual(output.count("\n"), self.shell.MAX_ADDR)

    def test_erase_invalid_parameter(self):
        params = [
            (99, 2),
            (0, -1),
            (75, 26),
            (25, 0),
            (100, 1),
            (3, 2.5),
            ("3", 2.5),
        ]

        for addr, size in params:
            with self.subTest(f"ssd E {addr} {size}"):
                self.assertIsNone(self.shell.erase(addr, size))

    def test_erase_valid_parameter(self):
        params = [
            (99, 1),
            (3, 5),
            (0, 2),
            (0, 100),
        ]

        for addr, size in params:
            with self.subTest(f"ssd E {addr} {size}"):
                output = self.shell.erase(addr, size)

                self.assertEqual(output, self.shell.SUCCESS)

    def test_erase_range_invalid_parameter(self):
        params = [
            (5, 2),
            (99, 99),
            (99, 101),
            (3, 5.5),
            ("3", 5.5),
        ]

        for start_addr, end_addr in params:
            with self.subTest(f"erase_range {start_addr} {end_addr}"):
                self.assertIsNone(self.shell.erase_range(start_addr, end_addr))

    def test_erase_range_valid_parameter(self):
        params = [
            (99, 100),
            (35, 36),
            (0, 2),
            (0, 100),
        ]

        for start_addr, end_addr in params:
            with self.subTest(f"erase_range {start_addr} {end_addr}"):
                output = self.shell.erase_range(start_addr, end_addr)

                self.assertEqual(output, self.shell.SUCCESS)
