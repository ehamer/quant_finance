import numpy as np


def calc_stats(a_equity):
    """
    calc_stats: given a 1-d array of equity, calculate, the annual return, sharpe ratio, sortino ratio,
    annual volatility, maximum draw down, begin index of max draw down, end index of max draw down, mar ratio,
    maximum time off peak, start index of max time off peak, end index of max time off peak

    the statistics are accurate, but it may not return everything if the length of the equity data is short
    """
    b_full_data = True
    a_ret = (a_equity[1:] - a_equity[:-1]) / a_equity[:-1]

    vola_daily = np.std(a_ret)
    vola_yearly = np.sqrt(252) * vola_daily

    index = np.cumprod(1 + a_ret)
    index_end = index[-1]

    ret_daily = np.exp(np.log(index_end) / a_ret.shape[0]) - 1
    ret_yearly = ((1 + ret_daily) ** 252) - 1.0
    sharpe_ratio = ret_yearly / vola_yearly

    a_down_ret = a_ret.copy()
    a_down_ret[a_down_ret > 0] = 0
    vola_downside = np.std(a_down_ret)
    vola_yearly_downside = vola_downside * np.sqrt(252)

    sortino = ret_yearly / vola_yearly_downside

    a_high_ret = a_equity.copy()

    a_test = np.ones((1, len(a_high_ret)))
    test_val = np.array_equal(a_high_ret, a_test[0])

    if test_val:
        b_full_data = False
        m_x = np.NaN
        m_ix = np.NaN
        max_dd = np.NaN
        mar = np.NaN
        max_time_off_peak = np.NaN
        mtop_start = np.NaN
        mtop_end = np.NaN
    else:
        for k in range(len(a_high_ret) - 1):
            if a_high_ret[k + 1] < a_high_ret[k]:
                a_high_ret[k + 1] = a_high_ret[k]

        under_water = a_equity / a_high_ret
        mi = np.min(under_water)
        m_ix = np.argmin(under_water)
        max_dd = 1 - mi
        try:
            # ebh: this needs to be fixed
            m_x = np.where(a_high_ret[0:m_ix - 1] == np.max(a_high_ret[0:m_ix - 1]))
            #        highList = highCurve.copy()
            #        highList.tolist()
            #        mX= highList[0:mIx].index(np.max(highList[0:mIx]))
            m_x = m_x[0][0]
            mar = ret_yearly / max_dd

            m_top = a_equity < a_high_ret
            m_top = np.insert(m_top, [0, len(m_top)], False)
            m_top_diff = np.diff(m_top.astype('int'))
            ix_start = np.where(m_top_diff == 1)[0]
            ix_end = np.where(m_top_diff == -1)[0]

            off_peak = ix_end - ix_start
            if len(off_peak) > 0:
                max_time_off_peak = np.max(off_peak)
                top_ix = np.argmax(off_peak)
            else:
                max_time_off_peak = 0
                top_ix = np.zeros(0)

            if np.not_equal(np.size(top_ix), 0):
                mtop_start = ix_start[top_ix] - 2
                mtop_end = ix_end[top_ix] - 1
            else:
                b_full_data = False
                mtop_start = np.NaN
                mtop_end = np.NaN
                mar = np.NaN
                max_time_off_peak = np.NaN
        except ValueError:
            b_full_data = False
            mtop_start = np.NaN
            mtop_end = np.NaN
            max_time_off_peak = np.NaN
            m_x = np.NaN
            mar = np.NaN

    if b_full_data:
        dct_stats = {'sharpe': sharpe_ratio, 'sortino': sortino, 'return_yearly': ret_yearly,
                     'vola_yearly': vola_yearly, 'max_dd': max_dd, 'max_dd_begin': int(m_x),
                     'max_dd_end': int(m_ix), 'mar': mar, 'max_time_off_peak': int(max_time_off_peak),
                     'max_time_off_peak_begin': int(mtop_start), 'max_time_off_peak_end': int(mtop_end)}
    else:
        dct_stats = {'sharpe': sharpe_ratio, 'sortino': sortino, 'return_yearly': ret_yearly,
                     'vola_yearly': vola_yearly, 'max_dd': max_dd}

    return dct_stats
