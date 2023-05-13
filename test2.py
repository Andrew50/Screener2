import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 

import yfinance as yf
from Data7 import Data as data
import datetime
from Plot import Plot as plot

df = pd.read_feather("C:/Screener/sync/traits.feather")
bar = []
bar = [199, df]
plot.create(bar)




#scan = pd.read_feather(r"C:\Screener\sync\todays_setups.feather")

#print(scan)


'''
df = data.get('AAPL','1min',datetime.datetime.now(),account = True)\

print(df)
'''
'''
import pandas as pd
import numpy as np
import io

data = '''
'''
Date Symbol Action Price
2020-03-01 AAPL Buy 80
2020-04-01 AAPL Sell 130
2020-05-01 AAPL Buy 90
2020-06-01 AAPL Sell 125
2020-07-01 AAPL Buy 125
2020-08-01 AAPL Sell 110
2020-09-01 AAPL Buy 95
2020-10-01 AAPL Sell 125
2020-11-01 AAPL Buy 125
2020-12-01 AAPL Sell 140
2021-01-01 AAPL Buy 115

2021-02-01 AAPL Sell 135
'''
'''

df = pd.read_csv(io.StringIO(data), delim_whitespace=True)

df['Date'] = pd.to_datetime(df['Date'])

buy = df[df['Action'] == 'Buy']
print(buy)
buy2 = df[['Date']].merge(buy,how='outer')
print(df[['Date']])
print(buy2)
sell = df[df['Action'] == 'Sell']
sell2 = df[['Date']].merge(sell,how='outer')

import mplfinance as mpf
import yfinance as yf

data = yf.download("AAPL", interval='1mo', start="2020-03-01", end="2021-03-01")
data.dropna(how='any', inplace=True)

ap = [mpf.make_addplot(buy2['Price'], type='scatter', marker='^', markersize=200, color='g'),
      mpf.make_addplot(sell2['Price'], type='scatter', marker='v', markersize=200, color='r')
     ]
      
mpf.plot(data, type='candle', ylabel='Candle', addplot=ap, volume=False)
'''



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

df = # Lists inside of a list. [Setup][]

colors = []
dfsByColor = []
for i in range(len(df)):
    if(df.iloc[i][2] not in colors):
        colors.append(df.iloc[i][2])
        
for i in range(len(colors)):
    colordf = df.loc[df[2] == colors[i]] 
    dfsByColor.append(colordf)

apds = []
for i in range(len(dfsByColor)):
    currentDf = dfsByColor[i].sort_values(by=0)

    


    
