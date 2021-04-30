import pandas as pd
import technical_indicators as ti


def find_id_nr4(df, low='Low', high='High', close='Adj Close'):
    in_day = ti.find_inday(df, low='Low', high='High')
    nr4 = ti.find_nr4(df, low='Low', high='High', close='Adj Close')
    atr = ti.calc_average_true_range(df, low, high, close, window=4)

    signal = list(in_day & nr4)
    price = df[high]
    stop = atr

    signal_df = pd.DataFrame({'Price': price, 'Stop': stop})
    signal_df.set_index(df.index + pd.DateOffset(days=1), inplace=True)
    signal_df = signal_df[signal]

    signal_df['Executed'] = False

    return signal_df


# ada_usd['Last ATR'] = ada_usd['ATR'].shift(1)
# ada_usd['Last Close'] = ada_usd['Adj Close'].shift(1)
# ada_usd['Buy Price'] = ada_usd['Last Close'] + 3 * ada_usd['Last ATR']
# ada_usd['Buy'] = ada_usd['High'] >= ada_usd['Buy Price'] 
