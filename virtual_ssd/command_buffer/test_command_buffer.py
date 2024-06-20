import unittest
import time
import os
from command_buffer import CommandBuffer


class TestCommandBuffer(unittest.TestCase):

    def setUp(self):
        self.__test_buffer_filename = f"test_buffer_{int(time.time())}"
        self.cb = CommandBuffer(self.__test_buffer_filename)

    def tearDown(self):
        if os.path.exists(self.__test_buffer_filename):
            os.remove(self.__test_buffer_filename)

    def test_buffer_existence(self):
        self.assertTrue(os.path.exists(self.__test_buffer_filename))

    def test_buffer_insert(self):
        cmds = [
            ("W", 1, "0x1234ABCD"),
            ("E", 1, 2),
            ("W", 2, "0x1234ABCD"),
            ("E", 2, 2),
        ]

        for cmd in cmds:
            self.cb.insert_cmd(*cmd)

        self.assertEqual(self.cb.get_buffer_contents(), cmds)

    def test_buffer_insert_overflow(self):
        cmds = [
            ("W", 1, "0x1234ABCD"),
            ("W", 2, "0x1234ABCD"),
            ("W", 3, "0x1234ABCD"),
            ("W", 4, "0x1234ABCD"),
            ("W", 5, "0x1234ABCD"),
            ("W", 6, "0x1234ABCD"),
            ("W", 7, "0x1234ABCD"),
            ("W", 8, "0x1234ABCD"),
            ("W", 9, "0x1234ABCD"),
            ("W", 10, "0x1234ABCD"),
            ("W", 11, "0x1234ABCD"),
        ]

        for cmd in cmds:
            ret = self.cb.insert_cmd(*cmd)

        self.assertEqual(self.cb.get_buffer_contents(), cmds[-1:])
        self.assertEqual(ret, cmds[0:10])

    def test_get_value(self):
        cmds = [
            ("E", 10, 10),
            ("W", 1, "0x1234FFFF"),
            ("W", 2, "0x5678FFFF"),
            ("W", 3, "0x9ABCFFFF"),
            ("E", 5, 5),
        ]

        for cmd in cmds:
            self.cb.insert_cmd(*cmd)

        self.assertEqual(self.cb.get_value(1), "0x1234FFFF")
        self.assertEqual(self.cb.get_value(2), "0x5678FFFF")
        self.assertEqual(self.cb.get_value(3), "0x9ABCFFFF")
        self.assertIsNone(self.cb.get_value(4))
        self.assertIsNone(self.cb.get_value(99))

    def test_get_value_erased(self):
        cmds = [
            ("W", 1, "0x1234FFFF"),
            ("W", 2, "0x5678FFFF"),
            ("W", 3, "0x9ABCFFFF"),
            ("E", 1, 2),
        ]

        for cmd in cmds:
            self.cb.insert_cmd(*cmd)

        self.assertEqual(self.cb.get_value(1), "0x00000000")

    def test_flush(self):
        cmds = [
            ("E", 10, 10),
            ("W", 1, "0x1234FFFF"),
            ("W", 2, "0x5678FFFF"),
            ("W", 3, "0x9ABCFFFF"),
            ("E", 5, 5),
        ]

        buffer_contents = self.cb.flush()

        self.assertEqual(self.cb.get_buffer_contents(), [])
