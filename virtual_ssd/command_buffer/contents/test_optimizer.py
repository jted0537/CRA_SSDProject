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

    def test_erase_after_write(self):
        cmds = [
            ("W", 1, "0x1"),
            ("W", 1, "0x2"),
            ("W", 1, "0x3"),
            ("W", 2, "0x4"),
            ("W", 2, "0x5"),
            ("W", 3, "0x6"),
            ("E", 2, 1),
        ]
        expected = [
            ("W", 1, "0x1"),
            ("W", 1, "0x2"),
            ("W", 1, "0x3"),
            ("W", 3, "0x6"),
            ("E", 2, 1),
        ]

        optimizer = ReduceWriteByErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_erase_duplication(self):
        cmds = [
            ("E", 1, 3),
            ("E", 5, 2),
            ("E", 1, 10),
            ("E", 30, 10),
        ]
        expected = [
            ("E", 1, 10),
            ("E", 30, 10),
        ]

        optimizer = ReduceEraseDuplication()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_adjacent_erase_1(self):
        cmds = [
            ("E", 1, 3),
            ("E", 3, 5),
            ("E", 20, 6),
            ("E", 26, 5),
        ]
        expected = [
            ("E", 1, 7),
            ("E", 20, 6),
            ("E", 26, 5),
        ]

        optimizer = MergeAdjacentErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_adjacent_erase_2(self):
        cmds = [
            ("E", 1, 3),
            ("E", 3, 5),
            ("E", 8, 1),
        ]
        expected = [
            ("E", 1, 8),
        ]

        optimizer = MergeAdjacentErase()

        self.assertEqual(optimizer.optimize(cmds), expected)
