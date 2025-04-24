import unittest
from output import Simulation
import io
import sys
import tempfile
import contextlib 

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

    def test_prop_alert_valid(self):
        test = Simulation(self._length, self._devices, self._propagates, self._alerts, self._cancellations)
        
        alerts = test.prop_alert()
        
        self.assertIn('@100: #1 SENT ALERT TO #2: test', alerts)
        self.assertIn('@200: #2 RECEIVED ALERT FROM #1: test', alerts)

    def test_prop_cancel(self):
        test = Simulation(self._length, self._devices, self._propagates, self._alerts, self._cancellations)

        cancels = test.prop_cancel()

        self.assertIn('@300: #1 SENT CANCELLATION TO #2: test', cancels)
        self.assertIn('@400: #2 RECEIVED CANCELLATION FROM #1: test', cancels)

    def test_run_correctly_outputs(self):
        test = Simulation(self._length, self._devices, self._propagates, self._alerts, self._cancellations)

        with io.StringIO() as vals, contextlib.redirect_stdout(vals):
            test.run()
            output = vals.getvalue()

        self.assertIn('@100: #1 SENT ALERT TO #2: test', output)
        self.assertIn('@200: #2 RECEIVED ALERT FROM #1: test', output)
        self.assertIn('@300: #1 SENT CANCELLATION TO #2: test', output)
        self.assertIn('@400: #2 RECEIVED CANCELLATION FROM #1: test', output)
        self.assertIn('@1000: END', output)
        


if __name__ == '__main__':
    unittest.main()


