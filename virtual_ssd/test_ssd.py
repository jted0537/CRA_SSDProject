from abc import ABC
from unittest import TestCase
from ssd import SSD


class TestSSD(TestCase):
    def test_print(self):
        pass

    def test_write_normal(self):
        self.ssd = SSD()

        addr = 20
        value = 0x1234ABCD

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, "SUCCESS")
