import logging
import numpy as np
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s: %(message)s [%(module)s:%(funcName)s:%(lineno)d]')


def open_orders(data, signals, strategy, product):
    
    transactions = pd.DataFrame(columns=['Date', 'Strategy', 'Product', 'Transaction', 'Price', 'Stop', 'Close Date'])

    for row in data.iterrows():
        current_date = row[0]

        if sum(signals.index == current_date) > 0:
            # logging.info(f'Current date is { current_date }')

            daily_signal = signals[signals.index == current_date] 

            order_price = float(daily_signal['Price'])
            order_stop = float(daily_signal['Stop'])

            day_low = row[1][2]
            day_high = row[1][1] 

            if day_high > order_price:
                # logging.info(f'We have order!')

                signals.loc[signals.index == current_date, 'Executed'] = True

                order = {'Date': current_date,
                         'Strategy': strategy,
                         'Product': product,
                         'Transaction': 'Buy',
                         'Price': order_price,
                         'Stop': order_stop}

                # logging.info(f'Order: { order } ')

                transactions = transactions.append(order, ignore_index=True)

    transactions.set_index('Date', inplace=True)
    
    return transactions


def estimate_profits(data, transactions):
    
    for row in data.iterrows():
        current_date = row[0]
        previous_date = (current_date + pd.DateOffset(days=-1)).strftime('%Y-%m-%d')

        day_low = row[1][2]

        ix_past_trans = (transactions.index < current_date)  & (transactions['Close Date'].isna())
        # past_transactions = transactions[]

        def retrieve_max_price(from_date, to_date):
            mp = max(list(data.loc[from_date:to_date, 'High']))
            return mp

        transactions.loc[ix_past_trans, 'Max Price'] = transactions[ix_past_trans].apply(lambda r: retrieve_max_price(r.name, previous_date), axis=1)

        transactions.loc[ix_past_trans, 'Sales Price'] = transactions.loc[ix_past_trans, 'Max Price'] - transactions.loc[ix_past_trans, 'Stop']

        transactions.loc[ix_past_trans, 'Sales'] = day_low <= transactions.loc[ix_past_trans, 'Sales Price']

        transactions.loc[ix_past_trans, 'Close Date'] =  transactions.loc[ix_past_trans, 'Sales'].apply(lambda r:  current_date if r else np.nan)
    

        print(f'\ncurrent_date: { current_date }')
        print(f'past_transactions:\n { transactions[ix_past_trans] }')


        # if past_transactions.shape[0] > 0:
            # past_transactions['Days Open'] = (current_date - past_transactions.index).days

            # open_date = past_transactions.index
            # days_open = past_transactions['Days Open'][0]
            # days_open_range = pd.date_range(open_date[0], periods=days_open)

            # max_price = data.loc[str(days_open_range[0].date()):str(days_open_range[-1].date()), 'High'].max()

            # for transaction in past_transactions.iterrows():
            #     max_price = data.loc[str(days_open_range[0].date()):str(days_open_range[-1].date()), 'High'].max()

            # print(current_date)
            # print(past_transactions)
        


        # past_transactions.apply()
        
        
        # daily_position = past_transactions[past_transactions.index == current_date]


        # buy_price = float(daily_position['Price'])
        # stop = float(daily_position['Stop'])

        # day_low = row[1][2]

        

        # if day_low <= stop_price:
        #     logging.info(f'Sold')

            

        #     p_l = 0
            

        

        
        
        
    
    

                

                
                

