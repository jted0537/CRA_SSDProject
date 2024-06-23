import unittest
from optimizer import *


class TestOptimizer(unittest.TestCase):
    def test_write_duplication(self):
        cmds = [
            ("W", 1, "0x1"),
            ("W", 1, "0x2"),
            ("W", 1, "0x3"),
            ("W", 2, "0x4"),
            ("W", 2, "0x5"),
            ("W", 3, "0x6"),
        ]
        expected = [
            ("W", 1, "0x3"),
            ("W", 2, "0x5"),
            ("W", 3, "0x6"),
        ]

        optimizer = ReduceWriteDuplication()

        self.assertEqual(optimizer.optimize(cmds), expected)
