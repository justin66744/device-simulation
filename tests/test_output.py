import unittest
from output import Simulation
import io
import sys
import tempfile

class TestOutput(unittest.TestCase):
    def setUp(self):
        self._length = 1000
        self._devices = [1, 2, 3]
        self._propagates = {'1': ('2', '100'), '2': ('3', '150'), '3': ('1', '200')}
        self._alerts = {'1': ('test', '100')}
        self._cancellations = {'1': ('test', '300')}


    def test_initial_values(self):
        test = Simulation(self._length, self._devices, self._propagates, self._alerts, self._cancellations)

        self.assertEqual(test._length, self._length)
        self.assertEqual(test._devices, self._devices)
        self.assertEqual(test._propagates, self._propagates)
        self.assertEqual(test._alerts, self._alerts)
        self.assertEqual(test._cancellations, self._cancellations)