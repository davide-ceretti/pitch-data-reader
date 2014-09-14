"""
ADD ORDER
Field Name | Offset | Length | Data Type | Description
------------------------------------------------------
Timestamp  | 0      | 8      | Numeric   | Timestamp
Msg Type   | 8      | 1      | "A"       | Add Order
Order ID   | 9      | 12     | Base 36   | Order Identifier
Site Indic | 21     | 1      | Alpha     | [B]uy or [S]Ell
Shares     | 22     | 6      | Numeric   | N. of Shares added
Stock Symb | 28     | 6      | Alpha     | Stock Symbol
Price      | 34     | 10     | Numeric   | Limit order Price
Display    | 44     | 1      | Alpha     | "Y" = Displayed in SIP

Example:
[28800011][A][AK27GA0000DT][S][000100][SH    ][0000619200][Y]
"""


"""
EXECUTE ORDER
Field Name | Offset | Length | Data Type | Description
------------------------------------------------------
Timestamp  | 0      | 8      | Numeric   | Timestamp
Msg Type   | 8      | 1      | "E"       | Execute Order
Order ID   | 9      | 12     | Base 36   | Order Identifier
Exc Shares | 21     | 6      | Numeric   | Number of shares executed
Exc ID     | 27     | 12     | Base 36   | Execution Identifier

Example:
[28800318][E][AK27GA0000DT][000050][00001AQ00001]
"""


def pitch_parser(iterable):
    """
    Takes an iterable containing PITCH messages and returns a dictionary
    with all the symbols as keys and all the executed volume as values
    """
    add_orders = {}
    volume = {}
    for message in iterable:
        message_type = message[8]
        if message_type == 'A':
            stock_symbol = message[28:34].replace(' ', '')
            shares = message[22:28]
            order_id = message[9:21]
            data = {
                'shares': shares,
                'stock_symbol': stock_symbol
            }
            add_orders[order_id] = data
        if message_type == 'E':
            exc_shares = int(message[21:27])
            order_id = message[9:21]
            order_data = add_orders[order_id]
            stock_symbol = order_data['stock_symbol']
            if stock_symbol not in volume:
                volume[stock_symbol] = exc_shares
            else:
                volume[stock_symbol] += exc_shares

    return volume
