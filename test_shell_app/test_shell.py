import io
from unittest import TestCase
from unittest.mock import patch, Mock

from shell import Shell

INVALID_PARAMETER_TEXT = "INVALID PARAMETER\n"
EXCEPTION_OCCUR_TEXT = "EXCEPTION OCCUR"
TEST_VAL = "0x000000FF"
INVALID_TEST_VAL = "0x0000zz"
TEST_ADDR = 10
INVALID_TEST_ADDR = -10
LARGE_ADDR = 9999


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_and_write(self, mock_stdout):
        self.shell.read(addr=TEST_ADDR)
        self.shell.write(addr=TEST_ADDR, val=TEST_VAL)
        self.assertNotIn(EXCEPTION_OCCUR_TEXT, mock_stdout.getvalue())
        self.assertEqual(TEST_VAL, self.shell.read(addr=TEST_ADDR))

    def test_read_valid_input(self):
        mk = Mock(spec=Shell)
        mk.read.return_value = TEST_VAL

        self.assertEqual(TEST_VAL, mk.read(TEST_ADDR))

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_pos(self, mock_stdout):
        self.assertIsNone(self.shell.read(LARGE_ADDR))
        self.assertEqual(mock_stdout.getvalue(), "%s" % INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_read_invalid_input_neg(self, mock_stdout):
        self.assertIsNone(self.shell.read(INVALID_TEST_ADDR))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_input_addr(self, mock_stdout):
        self.assertIsNone(self.shell.write(INVALID_TEST_ADDR, TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_write_invalid_input_val(self, mock_stdout):
        self.assertIsNone(self.shell.write(TEST_ADDR, INVALID_TEST_VAL))
        self.assertEqual(mock_stdout.getvalue(), INVALID_PARAMETER_TEXT)

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
