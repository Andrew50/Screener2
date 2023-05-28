import time
from multiprocessing import Pool, current_process
import pandas as pd
from Scan import Scan as scan

import yfinance as yf
from Data7 import Data as data
import datetime
from Plot import Plot as plot



################dont delte!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
setups = pd.read_feather('C:/Screener/sync/setups.feather')


ep = setups[setups['Setup'] == 'EP'].reset_index(drop = True)


other = setups[setups['Setup'] != 'EP'].reset_index(drop = True)


ep['setup'] = 1

other['setup'] = 0


df = pd.concat([ep,other]).sample(frac = 1).reset_index(drop = True)



setups = pd.DataFrame()

setups['ticker'] = df['Ticker']

setups['date'] = df['Date']

setups ['setup'] = df['setup']

print(setups)


setups.to_feather('C:/Screener/setups/EP.feather')











