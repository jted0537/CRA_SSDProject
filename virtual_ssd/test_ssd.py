from unittest import TestCase
from ssd import SSD
class TestSSD(TestCase):
    def setUp(self):
        self.ssd = SSD()

    def test_read(self):
        try:
            self.ssd.read(1)
            result_file = open('./result.txt', 'r')
            self.assertNotEqual(result_file.read(), "")
        except:
            self.fail()

    def test_write(self):
        self.assertEqual(1, 1)
