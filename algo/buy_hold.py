import numpy as np

from algo.algo_base import AlgoBase
from util import price_data as upd


class BuyHold(AlgoBase):
    """
    buy and hold is the simplest algorithm and produces surprisingly good results
    on the first day possible, the equity is purchased and it is never sold
    """
    def __init__(self):
        super().__init__('Buy and Hold')
        return

    def _process_single(self, txt_ticker, dct_settings):
        tpl_data = dct_settings['tpl_data']
        i_lookback = dct_settings['lookback']
        if len(tpl_data[4]) < i_lookback:
            return [], [], [], []

        lst_equity, lst_date, lst_duration = self.process_data(BuyHold.run_backtest, dct_settings)
        if 0 == len(lst_equity):
            return [], [], [], []

        np_ret = np.array(lst_equity)
        dct_stats = upd.calc_stats(np_ret)

        self.print_results(txt_ticker, lst_duration, dct_settings, dct_stats)
        return lst_equity, lst_date, lst_duration, dct_settings

    @staticmethod
    def run_backtest(i_index, dct_settings):
        dct_settings['status'] = AlgoBase.BULL
        return AlgoBase.BULL

    @staticmethod
    def _get_settings():
        dct_settings = {'init_balance': 1000000, 'leverage': 1, 'slippage': 1.0, 'lookback': 21}

        return dct_settings

    def print_header(self):
        txt_header, _ = self._header_text()
        print(txt_header)
        return

    def print_results(self, txt_ticker, lst_duration, dct_settings, dct_stats):
        if not self.b_print_data:
            return

        _, txt_header_fmt = self._header_text()

        last_start_date = lst_duration[-1][0]
        if AlgoBase.BULL == dct_settings['status']:
            b_active = True
        else:
            b_active = False

        i_leverage = dct_settings['leverage']
        txt_out = txt_header_fmt.format(txt_ticker, lst_duration[0][0], "{0:.4f}".format(dct_stats['return_yearly']),
                                        "{0:.2f}".format(dct_stats['sharpe']),
                                        "{0:.2f}".format(dct_stats['vola_yearly']),
                                        "{0:.2f}".format(dct_stats['max_dd']), len(lst_duration), last_start_date,
                                        i_leverage, b_active)
        print(txt_out)

    @staticmethod
    def _header_text():
        txt_header = "Ticker\tFirst\tReturn\tSharpe\tVolatility\tDrawdown\tChanges\tRecent\tLeverage\tActive"
        txt_header_fmt = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}"

        return txt_header, txt_header_fmt
