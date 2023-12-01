import http
import http.client

import json
import os


def load_equity_price_history_from_file(txt_file):
    """
    the data is stored as a list of dictionaries, where each dict has these fields:
    date, open, high, low, close, volume.

    this data is transformed into a tpl where each of the above fields is stored in a list.
    this makes it simpler to process in the back test
    """
    try:
        fp = open(txt_file, 'r')
        lst_data = json.load(fp)
        fp.close()
    except FileNotFoundError:
        lst_data = None

    if lst_data:
        tpl = tuple_from_lst_data(lst_data)
    else:
        tpl = None

    return tpl


def tuple_from_lst_data(lst_data):
    lst_date = []
    lst_open = []
    lst_high = []
    lst_low = []
    lst_close = []
    lst_volume = []

    for i in range(0, len(lst_data)):
        lst_date.append(lst_data[i]['date'])
        lst_open.append(lst_data[i]['open'])
        lst_high.append(lst_data[i]['high'])
        lst_low.append(lst_data[i]['low'])
        lst_close.append(lst_data[i]['close'])
        lst_volume.append(lst_data[i]['volume'])

    tpl = (lst_date, lst_open, lst_high, lst_low, lst_close, lst_volume)

    return tpl


def retrieve_ticker_fundamentals(txt_ticker):
    """
    use the API provided by Tradier brokerage to retrieve the fundamental data for an equity ticker
    you will need an account with Tradier brokerage and they will provide the API_URL and the API_AUTHORIZATION key
    """

    base_url = os.environ['API_URL']
    '''
    https://api.tradier.com/beta/markets/fundamentals/company?symbols=MSFT
    '''
    url = '/beta/markets/fundamentals/company?symbols='+txt_ticker
    headers = {"Accept": "application/json", "Authorization": os.environ['API_AUTHORIZATION']}

    connection = http.client.HTTPSConnection(base_url, 443, timeout=30)
    connection.request('GET', url, None, headers)

    try:
        response = connection.getresponse()
        status = response.status
        if 200 == status:
            content = response.read()
            dct_data = json.loads(content.decode("utf-8"))
        else:
            txt_error = 'retrieve_ticker_fundamentals. API status:' + str(status) + '\treason:' + str(response.reason)
            print(txt_error)
            return False, None
    except Exception as e:
        print('retrieve_ticker_fundamentals ' + str(e))
        return False, None

    return True, dct_data


def retrieve_price_history_lst(txt_ticker, start_date, txt_interval):
    """
    use the API provided by Tradier brokerage to retrieve the price data (date, open, high, low, close, volume)
    for an equity ticker
    """
    HISTORY_KEY = 'history'
    DAY_KEY = 'day'

    base_url = os.environ['API_URL']
    url = '/v1/markets/history?symbol=' + txt_ticker + '&interval=' + txt_interval + '&start=' + start_date.strftime(
        "%Y-%m-%d")
    headers = {"Accept": "application/json", "Authorization": os.environ['API_AUTHORIZATION']}

    connection = http.client.HTTPSConnection(base_url, 443, timeout=30)
    connection.request('GET', url, None, headers)

    try:
        response = connection.getresponse()
        status = response.status
        if 200 == status:
            content = response.read()
            dct_data = json.loads(content.decode("utf-8"))
        else:
            txt_error = 'retrieve_price_history_dct. API status:' + str(status) + '\treason:' + str(response.reason)
            print(txt_error)

            return False, None
    except Exception as e:
        print('history API error:' + str(e))
        return False, None

    assert (0 < len(dct_data))
    assert (True == (HISTORY_KEY in dct_data))
    if None is dct_data[HISTORY_KEY]:
        # we received and HTTP 200, but no data
        return True, None

    my_data = dct_data[HISTORY_KEY][DAY_KEY]
    while True:
        if type(my_data) == dict:
            lst_data = [my_data]
            break
        else:
            lst_data = my_data

            i_index = -1
            for i in range(0, len(lst_data)):
                dct = lst_data[i]
                for keys in dct:
                    if dct[keys] == 'NaN':
                        i_index = i
                        break

            if -1 < i_index:
                del lst_data[i_index]
            else:
                break

    return True, lst_data
