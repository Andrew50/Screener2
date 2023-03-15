
from Data5 import Data as data
import datetime

lap = (datetime.datetime.now())


df = data.get("AAPL",'1min',True)

date = datetime.datetime(2012, 3, 6, 8, 37 , 0)

lap = (datetime.datetime.now())

index = data.findex(df,date)

print(datetime.datetime.now() - lap)

print(date)
print(df.iloc[index]['datetime'])



