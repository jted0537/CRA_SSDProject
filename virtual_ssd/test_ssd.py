import time
import os
from unittest import TestCase
from unittest.mock import patch

from ssd import SSD


class TestSSD(TestCase):
    def setUp(self):
        current_time = int(time.time())

        self.__test_nand_filename = f"test_nand_{current_time}"
        self.__test_result_filename = f"test_nand_{current_time}"

        self.ssd = SSD(self.__test_nand_filename, self.__test_result_filename)

    def tearDown(self):
        if os.path.exists(self.__test_nand_filename):
            os.remove(self.__test_nand_filename)

        if os.path.exists(self.__test_result_filename):
            os.remove(self.__test_result_filename)

    @patch.object(SSD, "read")
    def test_read_mock(self, mk):
        def read(addr):
            if not 0 < addr < SSD.MAX_ADDR:
                raise TypeError
            return "0x88888888"

        mk.side_effect = read
        self.assertEqual(self.ssd.read(88), "0x88888888")
        with self.assertRaises(Exception):
            self.ssd.read(888)

    def test_read_real(self):
        try:
            self.assertEqual(self.ssd.read(1), SSD.SUCCESS)
            with open(self.__test_result_filename, "r") as f:
                self.assertEqual(f.read(), SSD.INIT_DATA)
        except:
            self.fail()

    def test_write_normal(self):
        addr = 20
        value = "0x1234ABCD"

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, SSD.SUCCESS)
        self.assertEqual(self.ssd.read(addr), SSD.SUCCESS)
        with open(self.__test_result_filename, "r") as f:
            self.assertEqual(f.read(), value)

    def test_write_invalid_value(self):
        addr = 20
        value = 12345678

        ret = self.ssd.write(addr, value)

        self.assertEqual(ret, SSD.FAIL)
