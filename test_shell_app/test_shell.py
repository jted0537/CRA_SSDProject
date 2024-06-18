from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock
from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_print(self):
        pass

    @patch.object(Shell, "write")
    def test_full_write(self, mk):
        def write(addr, val):
            self.shell._lbas[addr] = val

        mk.side_effect = write

        self.shell.full_write(0x12345678)
        self.assertEqual(self.shell._lbas, [0x12345678] * 100)
