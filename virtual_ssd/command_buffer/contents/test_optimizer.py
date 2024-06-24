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

    def test_merge_erase_1(self):
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

        optimizer = MergeErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_erase_2(self):
        cmds = [
            ("E", 1, 3),
            ("E", 3, 5),
            ("E", 8, 1),
        ]
        expected = [
            ("E", 1, 8),
        ]

        optimizer = MergeErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_erase_3(self):
        cmds = [
            ("E", 12, 3),
            ("E", 10, 2),
        ]
        expected = [
            ("E", 10, 5),
        ]

        optimizer = MergeErase()

        self.assertEqual(optimizer.optimize(cmds), expected)

    def test_merge_erase_4(self):
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

    def test_shrink_erase_1(self):
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

    def test_shrink_erase_2(self):
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

    def test_shrink_erase_3(self):
        cmds = [
            ("E", 18, 5),
            ("W", 20, "0xABCDABCD"),
            ("W", 22, "0xABCDABCD"),
            ("W", 18, "0x12341234"),
        ]
        expected = [
            ("E", 19, 3),
            ("W", 20, "0xABCDABCD"),
            ("W", 22, "0xABCDABCD"),
            ("W", 18, "0x12341234"),
        ]

        optimizer = ShrinkErase()

        self.assertEqual(optimizer.optimize(cmds), expected)
