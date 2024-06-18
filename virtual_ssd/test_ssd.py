from unittest import TestCase
from unittest.mock import patch

from ssd import SSD

class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD()

    @patch.object(SSD, "read")
    def test_read_mock(self, mk):
        def read(addr):
            if not 0 < addr < SSD.MAX_ADDR:
                raise TypeError
            return 0x88888888

        mk.side_effect = read
        self.assertEqual(self.ssd.read(88),  0x88888888)
        with self.assertRaises(Exception):
            self.ssd.read(888)

    def test_read_real(self):
        try:
            self.assertEqual(self.ssd.read(1), SSD.READ_SUCCESS)
        except:
            self.fail()

    def test_write_normal(self):
        addr = 20
        value = 0x1234ABCD

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, "SUCCESS")
