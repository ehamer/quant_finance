import numpy as np

from algo.algo_base import AlgoBase
from util import price_data as upd

import copy


class MeanReversion(AlgoBase):
    def __init__(self):
        super().__init__('MR')
        self.lst_ma = [10, 20, 30, 40, 50]
        self.lst_std = [1.0, 1.5, 2.0, 2.5, 3.0]
        return

    """
    process with a single set of backtest parameters based on dct_settings
    """
    def _process_single(self, txt_ticker, dct_settings):
        tpl_data = dct_settings['tpl_data']
        i_lookback = dct_settings['lookback']
        if len(tpl_data[4]) < i_lookback:
            return [], [], [], []

        lst_equity, lst_date, lst_duration = AlgoBase.process_data(MeanReversion.run_backtest, dct_settings)
        if 0 == len(lst_equity):
            return [], [], [], []

        np_ret = np.array(lst_equity)
        dct_stats = upd.calc_stats(np_ret)

        self.print_results(txt_ticker, lst_duration, dct_settings, dct_stats)
        return lst_equity, lst_date, lst_duration, dct_settings

        return lst_equity, lst_date, lst_duration, dct_settings

    """
    process all backtest parameters and either return thr results of the algorithm with the best sharpe ration,
    or return the results of all the back tests
    """
    def _process_single_full(self, txt_ticker, dct_settings):
        tpl_data = dct_settings['tpl_data']
        lst_date = tpl_data[0]
        i_lookback = dct_settings['lookback']
        if i_lookback > len(lst_date):
            return False, None

        tpl_best = None
        lst_ret = []
        for i_ma in self.lst_ma:
            for f_std in self.lst_std:
                dct_settings['mr_ma_bt'] = i_ma
                dct_settings['mr_std_bt'] = f_std
                dct_settings['state_data'] = {}
                lst_equity, lst_date, lst_duration = AlgoBase.process_data(MeanReversion.run_backtest, dct_settings)
                if 0 == len(lst_equity):
                    continue

                np_ret = np.array(lst_equity)
                dct_stats = upd.calc_stats(np_ret)

                if self.b_best_only:
                    if tpl_best:
                        if tpl_best[3]['sharpe'] < dct_stats['sharpe']:
                            tpl_best = (copy.copy(lst_equity), copy.copy(lst_duration),
                                        copy.deepcopy(dct_settings), copy.deepcopy(dct_stats))
                    else:
                        tpl_best = (copy.copy(lst_equity), copy.copy(lst_duration), copy.deepcopy(dct_settings),
                                    copy.deepcopy(dct_stats))
                else:
                    self.print_results(txt_ticker, lst_duration, dct_settings, dct_stats)
                    tpl = (lst_equity, lst_duration, dct_settings, dct_stats)
                    lst_ret.append(tpl)

        if self.b_best_only and tpl_best:
            lst_ret.append(tpl_best)
            self.print_results(txt_ticker, tpl_best[1], tpl_best[2], tpl_best[3])

        return True, lst_ret

    """
    this is called for each day we have data for. based on the band produced by the moving average, +/- the standard
    deviation.  when the price exceeds the high end, it is considered bearish, and when the price drops below the low 
    end, it is considered bullish 
    """
    @staticmethod
    def run_backtest(i_index, dct_settings):
        if dct_settings['mr_ma_bt'] > i_index:
            dct_settings['status'] = AlgoBase.BULL
            return AlgoBase.BULL

        f_std_delta = dct_settings['mr_std_bt']
        i_ma = dct_settings['mr_ma_bt']
        tpl_data = dct_settings['tpl_data']
        lst_price = tpl_data[4]
        lst_price = lst_price[:i_index]
        lst_price = lst_price[-i_ma:]
        assert (i_ma == len(lst_price))

        f_sma = np.nansum(lst_price) / i_ma
        f_std = np.std(lst_price, ddof=1)

        f_high = f_sma + (f_std_delta * f_std)
        f_low = f_sma - (f_std_delta * f_std)

        i_status = AlgoBase.BULL
        f_price = lst_price[-1]
        if f_price >= f_high:
            i_status = AlgoBase.BEAR

        if f_price <= f_low:
            i_status = AlgoBase.BULL

        dct_settings['status'] = i_status
        return i_status

    """
    print the results of a back test, this includes the return and the back test parameters used in this backtest
    """
    def print_results(self, txt_ticker, lst_duration, dct_settings, dct_stats):
        if not self.b_print_data:
            return

        _, txt_header_fmt = self._header_text()

        i_ma = dct_settings['mr_ma_bt']
        f_std = dct_settings['mr_std_bt']
        i_leverage = dct_settings['leverage']
        tpl_data = dct_settings['tpl_data']

        last_start_date = lst_duration[-1][0]
        if AlgoBase.BULL == dct_settings['status']:
            b_active = True
        else:
            b_active = False

        txt_out = txt_header_fmt.format(txt_ticker, tpl_data[0][0], "{0:.4f}".format(dct_stats['return_yearly']),
                                        "{0:.4f}".format(dct_stats['sharpe']),
                                        "{0:.2f}".format(dct_stats['vola_yearly']),
                                        "{0:.2f}".format(dct_stats['max_dd']), i_ma, "{0:.2f}".format(f_std),
                                        len(lst_duration), last_start_date, i_leverage, b_active)
        print(txt_out)

    def print_header(self):
        txt_header, _ = self._header_text()
        print(txt_header)
        return

    @staticmethod
    def _header_text():
        txt_header = "Ticker\tFirst\tReturn\tSharpe\tVolatility\tDrawdown\tMA\tStd Dev\tChanges\tRecent\tLeverage" \
                     "\tActive"
        txt_header_fmt = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}"

        return txt_header, txt_header_fmt

    @staticmethod
    def _get_settings():
        dct_settings = {'init_balance': 1000000, 'leverage': 1, 'slippage': 0.5, 'mr_std_bt': 3.0, 'mr_ma_bt': 10,
                        'lookback': 252}

        return dct_settings
