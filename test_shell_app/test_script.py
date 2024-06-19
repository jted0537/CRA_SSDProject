from unittest import TestCase

from testapp1 import TestApp1
from testapp2 import TestApp2

TEST_VALUE = "0x12345678"


class TestScript(TestCase):
    def setUp(self):
        super().setUp()
        self.testApp1 = TestApp1(TEST_VALUE)
        self.testApp2 = TestApp2()

    def test_testapp1(self):
        self.assertTrue(self.testApp1.run())

    # test TestApp2 class
    def test_testapp2(self):
        self.assertTrue(self.testApp2.run())
