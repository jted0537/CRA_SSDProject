import unittest
from unittest import skip

from optimizer import *


class TestOptimizer(unittest.TestCase):
    def test_ignore_write_1(self):
        cmds = [
            ("W", 20, "0xABCDABCD"),
            ("W", 21, "0x12341234"),
            ("W", 20, "0xEEEEFFFF"),
        ]
        expected = [
            ("W", 21, "0x12341234"),
            ("W", 20, "0xEEEEFFFF"),
        ]

        optimizer = ReduceWriteDuplication()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_ignore_write_2(self):
        cmds = [
            ("W", 20, "0xABCDABCD"),
            ("W", 21, "0x12341234"),
            ("E", 18, 5),
        ]
        expected = [
            ("E", 18, 5),
        ]

        optimizer = ReduceWriteByErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_erase_1(self):
        cmds = [
            ("W", 20, "0xABCDABCD"),
            ("E", 10, 2),
            ("E", 12, 3),
        ]
        expected = [
            ("W", 20, "0xABCDABCD"),
            ("E", 10, 5),
        ]

        optimizer = MergeErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_narrow_range_of_erase_1(self):
        cmds = [
            ("E", 10, 4),
            ("E", 40, 5),
            ("W", 12, "0xABCD1234"),
            ("W", 13, "0x4BCD5351"),
        ]
        expected = [
            ("E", 10, 2),
            ("E", 40, 5),
            ("W", 12, "0xABCD1234"),
            ("W", 13, "0x4BCD5351"),
        ]

        optimizer = ShrinkErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_narrow_range_of_erase_2(self):
        cmds = [
            ("E", 50, 1),
            ("E", 40, 5),
            ("W", 50, "0xABCD1234"),
        ]
        expected = [
            ("E", 40, 5),
            ("W", 50, "0xABCD1234"),
        ]

        optimizer = ShrinkErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_erase(self):
        cmds = [
            ("E", 18, 5),
            ("E", 10, 5),
            ("E", 18, 4),
        ]
        expected = [
            ("E", 10, 5),
            ("E", 18, 5),
        ]

        optimizer = MergeErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_erase_duplication(self):
        cmds = [
            ("E", 5, 2),
            ("E", 1, 10),
        ]
        expected = [
            ("E", 1, 10),
        ]

        optimizer = ReduceEraseDuplication()

        self.assertEqual(optimizer.optimize(cmds), expected)

