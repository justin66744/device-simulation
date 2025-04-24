import os
import sys
import io
import unittest
from project1 import file_read
import pathlib
import tempfile

class TestProj1(unittest.TestCase):
    def create_temp_file(self, text):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(text)
            return temp_file.name

    def test_file_with_valid_file(self):
        text = """LENGTH 1500
                  DEVICE 1
                  DEVICE 2
                  PROPAGATE 1 2 150
                  PROPAGATE 2 1 200 
                  ALERT 1 test 200
                  CANCEL 1 test 450
                  """
        temp_path = self.create_temp_file(text)
        try:
            path = pathlib.Path(temp_path)
            length, devices, propagates, alerts, cancellations = file_read(path)
            
            self.assertEqual(length, 1500)
            self.assertEqual(devices, [1, 2])
            self.assertEqual(propagates, {'1': ('2', '150'), '2': ('1', '200')})
            self.assertEqual(alerts, {'1': ('test', '200')})
            self.assertEqual(cancellations, {'1': ('test', '450')})
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_file_with_invalid_file(self):
        non_existent_path = "/invalid/path.txt"

        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        path = pathlib.Path(non_existent_path)
        result = file_read(path)

        output = sys.stdout.getvalue()
        sys.stdout = original_stdout

        self.assertIsNone(result)
        self.assertEqual(output.strip(), "FILE NOT FOUND")

if __name__ == '__main__':
    unittest.main()