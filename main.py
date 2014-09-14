import operator


def pitch_parser(iterable):
    """
    Takes an iterable containing PITCH messages and returns a dictionary
    with all the symbols as keys and all the executed volume as values
    """
    add_orders = {}
    volume = {}
    for message in iterable:
        if message[0] == 'S':
            message = message[1:]
        message_type = message[8]
        if message_type == 'A':
            stock_symbol = message[28:34].replace(' ', '')
            shares = message[22:28]
            order_id = message[9:21]
            data = {
                'shares': int(shares),
                'stock_symbol': stock_symbol
            }
            add_orders[order_id] = data
        if message_type == 'E':
            exc_shares = int(message[21:27])
            order_id = message[9:21]
            try:
                order_data = add_orders[order_id]
            except KeyError:
                continue
            stock_symbol = order_data['stock_symbol']
            shares = order_data['shares']
            if stock_symbol not in volume:
                if exc_shares <= shares:
                    volume[stock_symbol] = exc_shares
                    order_data['shares'] -= exc_shares
            else:
                if exc_shares <= shares:
                    volume[stock_symbol] += exc_shares
                    order_data['shares'] -= exc_shares

    return volume


def extract_top_ten_symbols_from_volume(volume):
    sorted_volume = sorted(
        volume.iteritems(), key=operator.itemgetter(1), reverse=True
    )
    return tuple(sorted_volume[:10])
