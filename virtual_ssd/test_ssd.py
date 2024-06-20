import os
import unittest
import time
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

    @unittest.skip
    def test_real_nand_init(self):
        if os.path.exists(SSD.DATA_LOC):
            os.remove(SSD.DATA_LOC)
        self.ssd.__init__()
        self.assertTrue(os.path.exists(SSD.DATA_LOC))

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

    def test_read_wrong_type_of_address(self):
        self.assertEqual(self.ssd.read("88"), SSD.FAIL)

    def test_read_real(self):
        self.assertEqual(self.ssd.read(1), SSD.SUCCESS)

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

    def test_erase_real(self):
        addr = 20

        ret = self.ssd.erase(addr, 1)
        self.assertEqual(ret, SSD.SUCCESS)
        self.assertEqual(self.ssd.read(addr), SSD.SUCCESS)
        with open(self.__test_result_filename, "r") as f:
            self.assertEqual(f.read(), "0x00000000")


if __name__ == "__main__":
    unittest.main()
