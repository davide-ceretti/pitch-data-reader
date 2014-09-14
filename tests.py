import unittest
from collections import OrderedDict

from main import pitch_parser, extract_top_ten_symbols_from_volume


def create_add_order(**kwargs):
    defaults = [
        ('prefix', 'S'),
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
        ('prefix', 'S'),
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
            "S28800011AAK27GA0000DTS000100SH    0000619200Y"
        )

    def test_create_add_order_override_shares(self):
        order = create_add_order(shares="999999")

        self.assertEqual(
            order,
            "S28800011AAK27GA0000DTS999999SH    0000619200Y"
        )

    def test_create_execute_order_default(self):
        order = create_execute_order()

        self.assertEqual(
            order,
            "S28800011EAK27GA0000DT00004000001AQ00001"
        )

    def test_create_execute_order_override_order_id(self):
        order = create_execute_order(order_id="XXXXXXXXXXXX")

        self.assertEqual(
            order,
            "S28800011EXXXXXXXXXXXX00004000001AQ00001"
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

    def test_add_order_and_execute_order_over_limit_second_exec(self):
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

    def test_add_order_and_execute_order_over_limit_first_exec(self):
        data = [
            create_add_order(
                stock_symbol='DAV   ', order_id='QQQWWWEEERRR', shares='000200'
            ),
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000201'),
        ]

        result = pitch_parser(data)

        expected = {}
        self.assertDictEqual(result, expected)

    def test_execute_order_for_uknown_id(self):
        data = [
            create_execute_order(order_id='QQQWWWEEERRR', exec_shares='000100'),
        ]

        result = pitch_parser(data)

        expected = {}
        self.assertDictEqual(result, expected)


class TestExtractTopTenSymbolsFromVolume(unittest.TestCase):
    def _make_orders(self, initial_data):
        data = []
        for order_id, stock_symbol, shares in initial_data:
            add_order = create_add_order(
                stock_symbol=stock_symbol, order_id=order_id, shares=shares
            )
            exec_order = create_execute_order(
                order_id=order_id, exec_shares=shares
            )
            data.append(add_order)
            data.append(exec_order)
        return data

    def test_empty_volume(self):
        data = []
        volume = pitch_parser(data)

        result = extract_top_ten_symbols_from_volume(volume)

        expected = ()
        self.assertTupleEqual(result, expected)

    def test_volume_size_smaller_than_ten(self):
        args = [
            ('000000000001', 'DAV001', '100000'),
            ('000000000002', 'DAV002', '200000'),
            ('000000000003', 'DAV003', '010000'),
        ]

        volume = pitch_parser(self._make_orders(args))

        result = extract_top_ten_symbols_from_volume(volume)

        expected = (
            ('DAV002', 200000),
            ('DAV001', 100000),
            ('DAV003', 10000),
        )
        self.assertTupleEqual(result, expected)

    def test_volume_size_greater_than_ten(self):
        args = [
            ('000000000001', 'DAV001', '100000'),
            ('000000000002', 'DAV002', '200000'),
            ('000000000003', 'DAV003', '010000'),
            ('000000000004', 'DAV004', '900000'),
            ('000000000005', 'DAV005', '100001'),
            ('000000000006', 'DAV006', '200001'),
            ('000000000007', 'DAV007', '010001'),
            ('000000000008', 'DAV008', '900001'),
            ('000000000009', 'DAV009', '100002'),
            ('000000000010', 'DAV010', '200002'),
            ('000000000011', 'DAV011', '010002'),
            ('000000000012', 'DAV012', '900002'),
            ('000000000013', 'DAV013', '000001'),
            ('000000000014', 'DAV014', '999999'),
        ]

        volume = pitch_parser(self._make_orders(args))

        result = extract_top_ten_symbols_from_volume(volume)

        expected = (
            ('DAV014', 999999),
            ('DAV012', 900002),
            ('DAV008', 900001),
            ('DAV004', 900000),
            ('DAV010', 200002),
            ('DAV006', 200001),
            ('DAV002', 200000),
            ('DAV009', 100002),
            ('DAV005', 100001),
            ('DAV001', 100000),

        )
        self.assertTupleEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
