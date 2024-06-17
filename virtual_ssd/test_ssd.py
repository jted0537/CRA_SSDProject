from abc import ABC
from ssd import SSD


class TestSSD(ABC):
    def test_print(self):
        pass

    def test_write_normal(self):
        self.ssd = SSD()

        addr = 20
        value = 0x1234ABCD

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, "SUCCESS")

    def test_write_invalid_addr(self):
        self.ssd = SSD()

        addr = 101
        value = 0x1234ABCD

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, "INVALID_ADDR")
