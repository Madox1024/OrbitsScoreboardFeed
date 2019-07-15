import unittest

from util import calc_milisec


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_time_parser(self):
        self.assertEqual(1, calc_milisec("00:00:00.001"))
        self.assertEqual(2, calc_milisec("00:00:00.002"))
        self.assertEqual(3, calc_milisec("00:00:00.003"))

        self.assertEqual(1100, calc_milisec("00:00:01.100"))
        self.assertEqual(61000, calc_milisec("00:01:01.000"))


if __name__ == '__main__':
    unittest.main()
