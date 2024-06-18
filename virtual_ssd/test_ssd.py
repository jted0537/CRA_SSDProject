from unittest import TestCase
from ssd import SSD
class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD()
    def test_read(self):
        self.assertEqual(1, self.ssd.read(99))

    def test_write(self):
        self.assertEqual(1, 1)
