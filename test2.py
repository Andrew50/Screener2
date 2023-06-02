import time
from multiprocessing import Pool, current_process
import pandas as pd
from Scan import Scan as scan

import yfinance as yf
from Data7 import Data as data
import datetime
from Plot import Plot as plot





df = data.get('yang')

print(df)


'''
setuptype = 'MR'
################dont delte!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
setups = pd.read_feather('C:/Screener/sync/setups.feather')
setups2 = pd.read_feather('C:/Screener/sync/allsetups.feather')

print(setups)

#ep = setups[setups['Setup'] == 'EP'].reset_index(drop = True)


ep = setups2[setups2['Setup'] == setuptype].reset_index(drop = True)


#ep = pd.concat([ep,ep2]).reset_index(drop = True)

other = setups[setups['Setup'] != setuptype].reset_index(drop = True)


ep['setup'] = 1

other['setup'] = 0


df = pd.concat([ep,other]).sample(frac = 1).reset_index(drop = True)



setups = pd.DataFrame()

setups['ticker'] = df['Ticker']

setups['date'] = df['Date']

setups ['setup'] = df['setup']

print(setups)


gud = setups[setups['setup'] == 1].reset_index(drop = True)
print(len(gud))

setups.to_feather('C:/Screener/setups/' + setuptype + '.feather')


'''








