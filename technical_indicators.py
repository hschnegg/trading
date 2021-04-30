import numpy as np
import pandas as pd


def calc_return(p1=None, p2=None, df=None, price='Adj Close', calc_log_ret=True, log_ret=None):
    if p1 is not None and p2 is not None:
        if calc_log_ret:
            ret = np.log(p2 / p1)
        else:
            ret = (p2 - p1) / p1
        return ret
    if df is not None:
        df = df.copy()
        df['last_close'] = df[price].shift(1)
        df['ret'] = calc_return(p1=df['last_close'], p2=df[price])
        return df['ret']
    if log_ret is not None:
        ret = np.exp(log_ret) - 1
        return ret


## https://en.wikipedia.org/wiki/Average_true_range
def calc_true_range(df, low='Low', high='High', close='Adj Close'):
    df = df.copy()
    df['last_close'] = df[close].shift(1)
    df['tr'] = df[[high, 'last_close']].max(axis=1) - df[[low, 'last_close']].min(axis=1)
    return df['tr']


## https://towardsdatascience.com/trading-toolbox-01-sma-7b8e16bd9388
def calc_sma(df, col, window):
    sma = df[col].rolling(window=window).mean()
    return sma


## https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
def calc_wma(df, col, window):
    weights = np.arange(1, window + 1)
    wma = df[col].rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
    return wma


## https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
def calc_ema(df, col, window):
    ema = df[col].ewm(span=window, adjust=False).mean()
    return ema


## https://en.wikipedia.org/wiki/Average_true_range
def calc_average_true_range(df, low, high, close, window):
    df = df.copy()
    df['tr'] = calc_true_range(df, low, high, close)
    atr = calc_ema(df, 'tr', window)
    return atr


def find_streak(df, price):
    df = df.copy()
    df['log_ret'] = calc_return(df=df, price=price, calc_log_ret=True, log_ret=None)
    
    current_sign = 999
    running_total = 0
    streak_run = []
    streak_start = df.shape[0] * [np.nan]
    streak_start_ix = 0
    
    for ix, e in enumerate(df['log_ret']):
        if np.sign(e) == current_sign:
            running_total = running_total + e
        else:
            streak_start[streak_start_ix] = running_total
            running_total = e
            current_sign = np.sign(e)
            streak_start_ix = ix
            
        streak_run.append(running_total)
    
    return streak_start, streak_run


def calc_min_n(df, col, window):
    min_n = df[col].rolling(window=window).min()
    return min_n


def calc_max_n(df, col, window):
    min_n = df[col].rolling(window=window).max()
    return min_n


def find_inday(df, low='Low', high='High'):
    df = df.copy()
    df['last_high'] = df[high].shift(1)
    df['last_low'] = df[low].shift(1)
    in_day = df.apply(lambda row: (row[high] < row['last_high']) and row[low] > row['last_low'], axis=1)
    
    return in_day


def find_nr4(df, low='Low', high='High', close='Adj Close'):
    df = df.copy()
    df['tr'] = calc_true_range(df, low, high, close)
    nr4 = calc_min_n(df, 'tr', 4) == df['tr']
    
    return nr4


