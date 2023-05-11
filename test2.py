import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 

import yfinance as yf
from Data7 import Data as data
import datetime



df = pd.read_feather(r"C:\Screener\sync\pnl.feather").set_index('datetime', drop = True)
print(df.index[-1])


'''

df = data.get('VERV','1min')
#index = data.findex(df,'2022-11-09 09:31:00')
print(df)
'''
'''


df = pd.read_feather(r"C:\Screener\tmp\full_ticker_list.feather")




#df.iat[9328,0] = '^VIX'
ticker = '^VIX'



add = pd.DataFrame({
            
                'Ticker': [ticker]
                
                })


df = pd.concat([df,add])

df = df.reset_index(drop = True)
print(df)




'''

'''
df = pd.read_feather(r"C:\Screener\tmp\pnl\pnl.feather")

df.to_csv(r"C:\Screener\tmp\pnl\pnlgod.csv")

'''

'''
df = pd.read_csv(r"C:\Screener\tmp\pnl\log.csv")
df['Datetime'] =  pd.to_datetime(df['Datetime'])

df.to_csv(r"C:/Screener/tmp/log.csv")


'''