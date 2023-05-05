import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 



df = pd.read_csv(r"C:\Screener\tmp\pnl\log.csv")
df['Datetime'] =  pd.to_datetime(df['Datetime'])


print(type(df.iat[1,0]))
print(type(df.iat[1,1]))
print(type(df.iat[1,2]))
print(type(df.iat[1,3]))
print(df)



df.to_feather(r"C:\Screener\tmp\pnl\log.feather")



