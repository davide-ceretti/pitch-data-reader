import unittest

from main import pitch_parser


class TestPitchParser(unittest.TestCase):
    def test_no_orders(self):
        data = []

        result = pitch_parser(data)

        self.assertDictEqual(result, {})

    def test_add_order(self):
        data = ["28800011AAK27GA0000DTS000100SH    0000619200Y"]

        result = pitch_parser(data)

        self.assertDictEqual(result, {})

    def test_add_order_and_execute_order(self):
        data = [
            "28800011AAK27GA0000DTS000100SH    0000619200Y",
            "28800318EAK27GA0000DT00004000001AQ00001"
        ]

        result = pitch_parser(data)

        expected = {"SH": 40}
        self.assertDictEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
