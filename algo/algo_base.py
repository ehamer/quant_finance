import os

from util import shared as sh


class AlgoBase:
    BULL = 1
    BEAR = -1
    NEUTRAL = 0

    LONG = BULL
    SHORT = BEAR

    NO_ACTION = 0
    BUY = 1
    SELL = 2
    SHORT = 3
    SHORT_COVER = 4

    SELL_THEN_SHORT = 10
    SHORT_COVER_THEN_BUY = 11

    def __init__(self, txt_name):
        self.txt_data_path = os.getcwd() + os.sep + 'data' + os.sep
        self.txt_name = txt_name

        self.b_print_data = True
        self.b_best_only = False

    def set_print_data(self, b_print):
        self.b_print_data = b_print

    def set_best_only(self, b_best):
        self.b_best_only = b_best

    """
    run a single backtest based on the parameters in dct_settings
    """
    def process_ticker(self, txt_ticker, dct_settings):
        txt_file_fmt = self.txt_data_path + "{0}.json"
        txt_file = txt_file_fmt.format(txt_ticker)
        tpl_data = sh.load_equity_price_history_from_file(txt_file)
        if not tpl_data:
            return [], [], [], []

        if dct_settings:
            dct_settings['tpl_data'] = tpl_data
        else:
            dct_settings = self._get_settings()
            dct_settings['tpl_data'] = tpl_data

        lst_equity, lst_date, lst_duration, dct_settings = self._process_single(txt_ticker, dct_settings)
        return lst_equity, lst_date, lst_duration, dct_settings

    """
    run backtests based on all combinations of the backtest parameters
    """
    def process_ticker_full(self, txt_ticker, dct_settings):
        txt_file_fmt = self.txt_data_path + "{0}.json"
        txt_file = txt_file_fmt.format(txt_ticker)
        tpl_data = sh.load_equity_price_history_from_file(txt_file)
        if not tpl_data:
            return False, None

        if dct_settings:
            dct_settings['tpl_data'] = tpl_data
        else:
            dct_settings = self._get_settings()
            dct_settings['tpl_data'] = tpl_data

        b_ret, lst_ret = self._process_single_full(txt_ticker, dct_settings)
        return b_ret, lst_ret

    """
    process_data performs the back test by iterating through each day of data for the equity
    if an equity is bought or sold short, then the change in value is calculated
    
    the return value is the list of equity values, the list of daily dates, and a list indicating the start date,
    initial value, end date, final equity value and the investment status for that period.  1 is a buy/hold, 
    0 is no position, and -1 is a short sale/hold
    
    f_trans_slippage is used to approximate trading costs.  if it is equal to 1.0, we will buy at the highest price, 
    and sell at the lowest price.  if it is 0.0 we will buy/sell at the open price which is the target.  any fraction 
    between 0.0 and 1.0 will be result in a buy price of open_price + f_trans_slippage * (high_price - open_price)
    """
    @staticmethod
    def process_data(current_status, dct_settings):
        f_trans_slippage = dct_settings['slippage']
        i_leverage = dct_settings['leverage']
        tpl_data = dct_settings['tpl_data']
        if not tpl_data:
            return [], [], []

        lst_equity = []
        lst_date = []
        lst_duration = []

        lst_date_org = tpl_data[0]
        lst_close_price = tpl_data[4]

        i_curr_status = current_status(0, dct_settings)
        lst_equity.append(dct_settings['init_balance'])
        txt_date = lst_date_org[0]

        tpl_duration = (txt_date, lst_equity[0])
        next_task = AlgoBase.NO_ACTION
        lst_date.append(txt_date)
        i = 1

        while i < len(lst_close_price):
            assert len(lst_date) == len(lst_equity)
            txt_date = lst_date_org[i]
            lst_date.append(lst_date_org[i])
            i_prev_status = i_curr_status
            i_curr_status = current_status(i, dct_settings)

            if AlgoBase.BUY == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_buy(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    assert AlgoBase.BEAR == i_curr_status  # or AlgoBase.BEAR == i_curr_status
                    # close out current tpl_duration
                    next_task = AlgoBase.SELL
                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if AlgoBase.SELL == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_sell(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    next_task = AlgoBase.BUY

                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if AlgoBase.SHORT == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_short(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    # close out current tpl_duration
                    next_task = AlgoBase.SHORT_COVER
                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if AlgoBase.SHORT_COVER == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_short_cover(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    assert AlgoBase.BEAR == i_curr_status
                    next_task = AlgoBase.SHORT
                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if AlgoBase.SELL_THEN_SHORT == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_sell(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta

                f_delta = AlgoBase.process_return_short(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    assert AlgoBase.BULL == i_curr_status
                    next_task = AlgoBase.BUY
                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if AlgoBase.SHORT_COVER_THEN_BUY == next_task:
                f_equity = lst_equity[-1]
                f_delta = AlgoBase.process_return_short_cover(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta

                f_delta = AlgoBase.process_return_buy(tpl_data, i, f_trans_slippage, i_leverage)
                f_equity *= f_delta
                tpl_duration = (txt_date, f_equity)
                lst_equity.append(f_equity)

                if i_curr_status != i_prev_status:
                    assert AlgoBase.BEAR == i_curr_status
                    next_task = AlgoBase.SELL
                    tpl_duration = (tpl_duration[0], tpl_duration[1], tpl_duration[0], tpl_duration[1], i_prev_status)
                    lst_duration.append(tpl_duration)
                    i = i + 1
                    continue

            if i_prev_status == i_curr_status:
                if AlgoBase.NEUTRAL == i_curr_status:
                    if AlgoBase.NO_ACTION == next_task:
                        f_equity = lst_equity[-1]
                        lst_equity.append(f_equity)
                else:
                    if AlgoBase.BULL == i_curr_status:
                        if AlgoBase.NO_ACTION == next_task:
                            f_delta = AlgoBase.leverage_return(tpl_data, i, AlgoBase.BULL, i_leverage)
                            f_equity = lst_equity[-1] * f_delta
                            lst_equity.append(f_equity)
                    else:
                        assert AlgoBase.BEAR == i_curr_status
                        if AlgoBase.NO_ACTION == next_task:
                            f_delta = AlgoBase.leverage_return(tpl_data, i, AlgoBase.BEAR, i_leverage)

                            f_equity = lst_equity[-1] * f_delta
                            lst_equity.append(f_equity)

                next_task = AlgoBase.NO_ACTION
            else:
                if AlgoBase.NEUTRAL == i_prev_status:
                    f_equity = lst_equity[i - 1]
                    lst_equity.append(f_equity)

                    tpl_duration = (tpl_duration[0], tpl_duration[1], txt_date, f_equity, AlgoBase.NEUTRAL)
                    lst_duration.append(tpl_duration)
                    if AlgoBase.BULL == i_curr_status:
                        next_task = AlgoBase.BUY
                    else:
                        assert AlgoBase.BEAR == i_curr_status
                        next_task = AlgoBase.SHORT

                if AlgoBase.BULL == i_prev_status:
                    f_delta = AlgoBase.leverage_return(tpl_data, i, AlgoBase.BULL, i_leverage)
                    # f_slippage = AlgoBase.calc_slippage(tpl_data, i, f_trans_slippage, i_leverage)
                    # f_slippage = 1.0 - f_trans_slippage
                    f_equity = lst_equity[-1] * f_delta
                    lst_equity.append(f_equity)
                    tpl_duration = (tpl_duration[0], tpl_duration[1], txt_date, f_equity, AlgoBase.BULL)
                    lst_duration.append(tpl_duration)

                    assert AlgoBase.NEUTRAL == i_curr_status or AlgoBase.BEAR == i_curr_status
                    if AlgoBase.BEAR == i_curr_status:
                        next_task = AlgoBase.SELL_THEN_SHORT
                    else:
                        next_task = AlgoBase.SELL

                if AlgoBase.BEAR == i_prev_status:
                    f_delta = AlgoBase.leverage_return(tpl_data, i, AlgoBase.BEAR, i_leverage)
                    f_equity = lst_equity[-1] * f_delta  # * f_slippage
                    lst_equity.append(f_equity)

                    tpl_duration = (tpl_duration[0], tpl_duration[1], txt_date, f_equity, AlgoBase.BEAR)
                    lst_duration.append(tpl_duration)

                    assert AlgoBase.NEUTRAL == i_curr_status or AlgoBase.LONG == i_curr_status
                    if AlgoBase.BULL == i_curr_status:
                        next_task = AlgoBase.SHORT_COVER_THEN_BUY
                    else:
                        next_task = AlgoBase.SHORT_COVER

            i = i + 1

        # ebh: form the last entry in the tpl_duration
        if 5 > len(tpl_duration):
            tpl_duration = (tpl_duration[0], tpl_duration[1], txt_date, f_equity, i_curr_status)
            lst_duration.append(tpl_duration)

        return lst_equity, lst_date, lst_duration

    """
    if the investment is leveraged, calculate the return accordingly
    """
    @staticmethod
    def leverage_return(daily_data, i, i_type, i_leverage):
        # the delta is the % wise difference from yesterday's close to today's high + plus the slippage
        assert 0 < i
        assert 0 < i_leverage

        _, f_prev_open, f_prev_high, f_prev_low, f_prev_close, _ = AlgoBase.data_from_tuple(daily_data, i - 1)
        _, f_open, f_high, f_low, f_close, _ = AlgoBase.data_from_tuple(daily_data, i)

        if AlgoBase.BULL == i_type:
            f_ret = ((f_close / f_prev_close) - 1.0) * i_leverage
        else:
            assert AlgoBase.BEAR == i_type
            f_ret = ((f_prev_close / f_close) - 1.0) * i_leverage

        f_ret = f_ret + 1.0
        return f_ret

    """
    extract the lists of data that we use from the tuple
    """
    @staticmethod
    def data_from_tuple(daily_data, index):
        txt_date = daily_data[0][index]
        f_open = daily_data[1][index]
        f_high = daily_data[2][index]
        f_low = daily_data[3][index]
        f_close = daily_data[4][index]
        i_vol = daily_data[5][index]

        return txt_date, f_open, f_high, f_low, f_close, i_vol

    """
    on a buy, calculate the return based on the difference between the high and the open and the slippage
    """
    @staticmethod
    def process_return_buy(tpl_data, i_index, f_trans_slippage, i_leverage):
        assert 0 < i_index
        assert 0 < i_leverage

        _, f_open, f_high, f_low, f_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index)

        f_buy = f_open + ((f_high - f_open) * f_trans_slippage)

        f_ret = (f_close / f_buy) - 1.0
        f_ret *= i_leverage
        f_ret += 1.0

        return f_ret

    @staticmethod
    def process_return_sell(tpl_data, i_index, f_trans_slippage, i_leverage):
        assert 0 < i_index
        assert 0 < i_leverage

        _, f_open, f_high, f_low, f_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index)
        _, f_prev_open, f_prev_high, f_prev_low, f_prev_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index - 1)
        f_sell = f_open - ((f_open - f_low) * f_trans_slippage)

        f_ret = (f_sell / f_prev_close) - 1.0
        f_ret *= i_leverage
        f_ret += 1.0

        return f_ret

    @staticmethod
    def process_return_short(tpl_data, i_index, f_trans_slippage, i_leverage):
        assert 0 < i_index
        assert 0 < i_leverage

        _, f_open, f_high, f_low, f_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index)
        f_buy = f_open - ((f_open - f_low) * f_trans_slippage)

        f_ret = (f_buy / f_close) - 1.0
        f_ret *= i_leverage
        f_ret += 1.0

        return f_ret

    @staticmethod
    def process_return_short_cover(tpl_data, i_index, f_trans_slippage, i_leverage):
        assert 0 < i_index
        assert 0 < i_leverage

        _, f_open, f_high, f_low, f_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index)
        _, f_prev_open, f_prev_high, f_prev_low, f_prev_close, _ = AlgoBase.data_from_tuple(tpl_data, i_index - 1)

        f_buy = f_open + ((f_high - f_open) * f_trans_slippage)

        f_ret = (f_prev_close / f_buy) - 1.0
        f_ret *= i_leverage
        f_ret += 1.0

        return f_ret
