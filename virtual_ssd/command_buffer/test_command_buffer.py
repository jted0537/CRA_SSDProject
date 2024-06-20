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
