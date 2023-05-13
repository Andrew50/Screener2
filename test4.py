import time
from multiprocessing import Pool, current_process
import pandas as pd
import Scan 

import yfinance as yf
from Data7 import Data as data
import datetime
import pandas as pd
import numpy as np
import io


df = pd.read_feather(r"C:/Screener/sync/log.feather")

print(df)
df.rename(columns={'Datetime':'datetime','Price':'price','Setup':'setup','Ticker':'ticker','Shares':'shares'}, inplace = True)


print(df)

df.to_feather(r"C:/Screener/sync/log.feather")