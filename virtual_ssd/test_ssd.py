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
        self.__test_result_filename = f"test_result_{current_time}"
        self.__test_buffer_filename = f"test_buffer_{current_time}"

        self.ssd = SSD(
            self.__test_nand_filename,
            self.__test_result_filename,
            self.__test_buffer_filename,
        )

    def tearDown(self):
        if os.path.exists(self.__test_nand_filename):
            os.remove(self.__test_nand_filename)

        if os.path.exists(self.__test_result_filename):
            os.remove(self.__test_result_filename)

        if os.path.exists(self.__test_buffer_filename):
            os.remove(self.__test_buffer_filename)

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

    def test_read__invalid_input(self):
        self.assertEqual(self.ssd.read("88"), SSD.FAIL)
        self.assertEqual(self.ssd.read(-1), SSD.FAIL)

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

        ret = self.ssd.write(addr, "0x88888888")
        self.assertEqual(ret, SSD.SUCCESS)
        ret = self.ssd.erase(addr, 1)
        self.assertEqual(ret, SSD.SUCCESS)
        self.assertEqual(self.ssd.read(addr), SSD.SUCCESS)
        with open(self.__test_result_filename, "r") as f:
            self.assertEqual(f.read(), "0x00000000")

    def test_erase_invalid_input(self):
        addr = 20
        self.assertEqual(self.ssd.erase(addr, 1000), SSD.FAIL)
        self.assertEqual(self.ssd.erase(addr, "10"), SSD.FAIL)
        self.assertEqual(self.ssd.erase(addr, -10), SSD.FAIL)
        self.assertEqual(self.ssd.erase(-10, 10), SSD.FAIL)
        self.assertEqual(self.ssd.erase("20", 10), SSD.FAIL)

    def test_write_buffer_overflow(self):
        last_cmd = []
        for i in range(1, 12):
            self.ssd.write(i, "0x0000000" + str(i % 10))
            last_cmd = [("W", i, "0x0000000" + str(i % 10))]

        self.assertEqual(last_cmd, self.ssd._buffer.flush())

    def test_erase_buffer_overflow(self):
        last_cmd = []
        for i in range(1, 12):
            self.ssd.erase(i, 1)
            last_cmd = [("E", i, 1)]

        self.assertEqual(last_cmd, self.ssd._buffer.flush())

    def test_buf_full(self):
        expected_list = []
        for i in range(1, 10):
            if i & 1:
                self.ssd.write(i, "0x0000000" + str(i % 10))
                expected_list.append(("W", i, "0x0000000" + str(i % 10)))
            else:
                self.ssd.erase(i, i)
                expected_list.append(("E", i, i))

        self.assertEqual(self.ssd._buffer.get_buffer_contents(), expected_list)

        self.assertEqual(self.ssd.read(6), SSD.SUCCESS)
        with open(self.__test_result_filename, "r") as f:
            self.assertEqual(f.read(), "0x00000000")

        self.assertEqual(self.ssd.read(7), SSD.SUCCESS)
        with open(self.__test_result_filename, "r") as f:
            self.assertEqual(f.read(), "0x00000007")

        self.ssd._buffer.flush()

    def test_flush(self):
        for i in range(1, 10):
            if i & 1:
                self.ssd.write(i, "0x0000000" + str(i % 10))
            else:
                self.ssd.erase(i, i)

        self.ssd._buffer.flush()
        self.assertEqual(self.ssd._buffer.get_buffer_contents(), [])


if __name__ == "__main__":
    unittest.main()
