import io
from unittest import TestCase
from unittest.mock import patch

from shell import Shell

INVALID_PARAMETER_TEXT = "INVALID PARAMETER\n"
EXCEPTION_OCCUR_TEXT = "EXCEPTION OCCUR"
INITIAL_VAL = "0x00000000"
VALID_TEST_VAL = "0x000000FF"
INVALID_TEST_VAL = "0x0000zz"
VALID_TEST_ADDR = 10
VALID_TEST_ADDR_WITHOUT_WRITE = 30
INVALID_TEST_ADDR_NEGATIVE = -10
INVALID_TEST_ADDR_LARGE = 9999


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_and_write(self, mock_stdout):
        self.shell.read(addr=VALID_TEST_ADDR)
        self.shell.write(addr=VALID_TEST_ADDR, val=VALID_TEST_VAL)
        self.assertNotIn(EXCEPTION_OCCUR_TEXT, mock_stdout.getvalue())
        self.assertEqual(VALID_TEST_VAL, self.shell.read(addr=VALID_TEST_ADDR))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_valid_addr_without_write(self, mock_stdout):
        self.shell.read(addr=VALID_TEST_ADDR)
        self.assertNotIn(EXCEPTION_OCCUR_TEXT, mock_stdout.getvalue())
        self.assertEqual(
            INITIAL_VAL, self.shell.read(addr=VALID_TEST_ADDR_WITHOUT_WRITE)
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_addr_large(self, mock_stdout):
        self.assertIsNone(self.shell.read(INVALID_TEST_ADDR_LARGE))
        self.assertEqual(mock_stdout.getvalue(), "%s" % INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_addr_negative(self, mock_stdout):
        self.assertIsNone(self.shell.read(INVALID_TEST_ADDR_NEGATIVE))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_addr_large(self, mock_stdout):
        self.assertIsNone(self.shell.write(INVALID_TEST_ADDR_LARGE, VALID_TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), "%s" % INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_addr_negative(self, mock_stdout):
        self.assertIsNone(self.shell.write(INVALID_TEST_ADDR_NEGATIVE, VALID_TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_val(self, mock_stdout):
        self.assertIsNone(self.shell.write(VALID_TEST_ADDR, INVALID_TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

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
