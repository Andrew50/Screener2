
from Data5 import Data as data
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import os
import datetime

lap = (datetime.datetime.now())


df = data.get("AAPL",'m')


date = datetime.date(2023, 3, 6)

#print(datetime.datetime.now() - lap)
lap = (datetime.datetime.now())

index = data.findex(df,date)

#print(datetime.datetime.now() - lap)




print(date)
print(df.iloc[index]['datetime'])
#print(df.iloc[index+1]['datetime'])


