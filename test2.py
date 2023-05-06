import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 

import yfinance as yf
from Data7 import Data as data





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

df.to_feather(r"C:\Screener\tmp\full_ticker_list.feather")


'''
df = pd.read_feather(r"C:\Screener\minute - Copy\META.feather")

print(df)

'''
df = pd.read_csv(r"C:\Screener\tmp\pnl\log.csv")
df['Datetime'] =  pd.to_datetime(df['Datetime'])


print(type(df.iat[1,0]))
print(type(df.iat[1,1]))
print(type(df.iat[1,2]))
print(type(df.iat[1,3]))
print(df)



df.to_feather(r"C:\Screener\tmp\pnl\log.feather")


'''
