
from Data5 import Data as data
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import os
import datetime

lap = (datetime.datetime.now())


df = data.get("AAPL",'17min')

date = datetime.datetime(2012, 3, 6, 11, 37 , 0)
#date = datetime.datetime(2023, 2, 6)
#print(datetime.datetime.now() - lap)
lap = (datetime.datetime.now())

index = data.findex(df,date)

print(datetime.datetime.now() - lap)




print(date)
print(df.iloc[index]['datetime'])
#print(df.iloc[index+1]['datetime'])


