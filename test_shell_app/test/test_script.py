import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest import TestCase

from Scripts.testapp1 import TestApp1
from Scripts.testapp2 import TestApp2
from Scripts.fullread10andcompare import FullRead10AndCompare
from Scripts.fullread3andcompare import FullRead3AndCompare
from Scripts.loopwriteandreadcompare import LoopWriteAndReadCompare
from Scripts.scenarioreturnsfail import ScenarioReturnsFail

TEST_VALUE = "0x12345678"


class TestScript(TestCase):
    def setUp(self):
        super().setUp()
        self.testApp1 = TestApp1(TEST_VALUE)
        self.testApp2 = TestApp2()
        self.fullread10andcompare = FullRead10AndCompare()
        self.fullread3andcompare = FullRead3AndCompare()
        self.loopwriteandreadcompare = LoopWriteAndReadCompare()
        self.scenarioreturnsfail = ScenarioReturnsFail()

    def test_testapp1(self):
        self.assertTrue(self.testApp1.run())

    # test TestApp2 class
    def test_testapp2(self):
        self.assertTrue(self.testApp2.run())

    def test_fullread10andcompare(self):
        self.assertTrue(self.fullread10andcompare.run())

    def test_fullread3andcompare(self):
        self.assertTrue(self.fullread3andcompare.run())

    def test_loopwriteandreadcompare(self):
        self.assertTrue(self.loopwriteandreadcompare.run())

    def test_scenarioreturnsfail(self):
        self.assertFalse(self.scenarioreturnsfail.run())
