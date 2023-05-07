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




'''


df = pd.read_feather(r"C:/Screener/tmp/log.feather")

df.to_csv(r"C:/Screener/tmp/log.csv")


