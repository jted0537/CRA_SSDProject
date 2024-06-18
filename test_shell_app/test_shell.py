import io
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock
from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_print(self):
        pass

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(Shell, "read")
    def test_full_read(self, mk, mk_stdout):
        def read(addr):
            print(self.shell._lbas[addr])

        mk.side_effect = read

        self.shell.full_read()
        self.assertIn("0\n0\n0\n0", mk_stdout.getvalue())
