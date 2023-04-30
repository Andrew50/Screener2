import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 



df = pd.read_feather("C:/Screener/tmp/setups.feather")
'''
df['gap'] = df['annotation']
df = df.drop(['adr','vol','q','1','2','3','10','time','annotation'], axis = 1)
df = df.rename(columns = {"gap":'annotation'})

df.to_feather(r"C:\Screener\tmp\setups.feather")

'''
print(df)