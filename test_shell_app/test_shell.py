from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock
from shell import Shell


class TestShell(TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_print(self):
        pass

    def test_full_write(self):
        mk = Mock(spec=Shell)
        mk._lbas = [0] * 100

        def write(addr, val):
            mk._lbas[addr] = val

        mk.write.side_effect = write

        mk.write(1, 100)
        print(mk._lbas)
        # mk.full_write = self.shell.full_write
        mk.full_write(0x12345678)

        self.assertEqual(mk._lbas, [0x12345678] * 100)
