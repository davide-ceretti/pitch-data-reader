import unittest
from collections import OrderedDict

from main import pitch_parser


def create_add_order(**kwargs):
    defaults = [
        ('timestamp', "28800011"),
        ('msg_type', "A"),
        ('order_id', "AK27GA0000DT"),
        ('site_indicator', "S"),
        ('shares', "000100"),
        ('stock_symbol', "SH    "),
        ('price', "0000619200"),
        ('display', "Y"),
    ]
    add_order_dict = OrderedDict()
    for key, value in defaults:
        add_order_dict[key] = value
    add_order_dict.update(**kwargs)
    return "".join(add_order_dict.itervalues())


def create_execute_order(**kwargs):
    defaults = [
        ('timestamp', "28800011"),
        ('msg_type', "E"),
        ('order_id', "AK27GA0000DT"),
        ('exec_shares', "000040"),
        ('exec_id', "00001AQ00001"),
    ]
    add_order_dict = OrderedDict()
    for key, value in defaults:
        add_order_dict[key] = value
    add_order_dict.update(**kwargs)
    return "".join(add_order_dict.itervalues())


class TestUtils(unittest.TestCase):
    def test_create_add_order_default(self):
        order = create_add_order()

        self.assertEqual(
            order,
            "28800011AAK27GA0000DTS000100SH    0000619200Y"
        )

    def test_create_add_order_override_shares(self):
        order = create_add_order(shares="999999")

        self.assertEqual(
            order,
            "28800011AAK27GA0000DTS999999SH    0000619200Y"
        )

    def test_create_execute_order_default(self):
        order = create_execute_order()

        self.assertEqual(
            order,
            "28800011EAK27GA0000DT00004000001AQ00001"
        )

    def test_create_execute_order_override_order_id(self):
        order = create_execute_order(order_id="XXXXXXXXXXXX")

        self.assertEqual(
            order,
            "28800011EXXXXXXXXXXXX00004000001AQ00001"
        )


class TestPitchParser(unittest.TestCase):
    def test_no_orders(self):
        data = []

        result = pitch_parser(data)

        self.assertDictEqual(result, {})

    def test_add_order(self):
        data = [create_add_order()]

        result = pitch_parser(data)

        self.assertDictEqual(result, {})

    def test_add_order_and_execute_order(self):
        data = [
            create_add_order(
                stock_symbol='DAV   ', order_id='QQQWWWEEERRR', shares='000200'
            ),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000110')
        ]

        result = pitch_parser(data)

        expected = {"DAV": 110}
        self.assertDictEqual(result, expected)

    def test_add_order_and_execute_order_multiple_times(self):
        data = [
            create_add_order(
                stock_symbol='DAV   ', order_id='QQQWWWEEERRR', shares='000200'
            ),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000110'),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000003'),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000005')
        ]

        result = pitch_parser(data)

        expected = {"DAV": 118}
        self.assertDictEqual(result, expected)

    def test_add_order_and_execute_order_over_limit(self):
        data = [
            create_add_order(
                stock_symbol='DAV   ', order_id='QQQWWWEEERRR', shares='000200'
            ),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000110'),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000091'),
        ]

        result = pitch_parser(data)

        expected = {"DAV": 110}
        self.assertDictEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
