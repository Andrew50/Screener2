




from tvDatafeed import TvDatafeed, Interval
from Scan import Scan as scan
import datetime
from pyarrow import feather
import pandas as pd
from Data7 import Data as data







#df = pd.read_feather(r"C:\Screener\tmp\todays_setups.feather")
#print(df)
date = '2022-02-02'
tf = 'd'

df = scan.get(date,tf,True)

df2 =  pd.read_csv('C:/Screener/tmp/full_ticker_list - backup.csv')

#print(len(df))
#print(len(df2))
god = []
for ticker in df.index.to_list():
    try:
        data.get(ticker)
    except:
        god.append(ticker)

print(god)