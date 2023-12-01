from algo.buy_hold import BuyHold
from algo.mr import MeanReversion


def process_buy_and_hold():
    dct_settings = {'init_balance': 1000000, 'leverage': 1, 'slippage': 1.0, 'lookback': 21}
    txt_ticker = 'AAPL'
    my_algo = BuyHold()
    my_algo.print_header()
    lst_equity, lst_date, lst_duration, dct_settings = my_algo.process_ticker(txt_ticker, dct_settings)


def process_mean_reversion():
    txt_ticker = 'AAPL'
    my_algo = MeanReversion()
    my_algo.print_header()
    b_ret, lst_ret = my_algo.process_ticker_full(txt_ticker, None)


def main():
    process_buy_and_hold()
    print()
    process_mean_reversion()
    return


if __name__ == '__main__':
    main()
