import unittest

from main import pitch_parser


class TestPitchParser(unittest.TestCase):
    def test_no_orders(self):
        data = []

        result = pitch_parser(data)

        self.assertDictEqual(result, {})

    def test_add_order(self):
        data = ["S28800011AAK27GA0000DTS000100SH    0000619200Y"]

        result = pitch_parser(data)

        self.assertDictEqual(result, {})


if __name__ == "__main__":
    unittest.main()
