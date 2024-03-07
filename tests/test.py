# run the test by running `python -m unittest tests/test.py`

import unittest
from datetime import datetime
from stool import first_day_of_month


# write some code to test functions in stool/core.py
class TestCore(unittest.TestCase):
    def test_first_day_of_month(self):
        f = first_day_of_month(datetime(2020, 2, 15))
        print(f)
        self.assertEqual(f, datetime(2020, 2, 1))
