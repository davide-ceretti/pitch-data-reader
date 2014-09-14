import unittest

from main import pitch_parser


class TestAddOrder(unittest.TestCase):
    def test_no_orders(self):
        result = pitch_parser('empty_data')

        self.assertDictEqual(result, {})


if __name__ == "__main__":
    unittest.main()
