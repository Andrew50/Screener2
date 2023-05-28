import time
from multiprocessing import Pool, current_process
import pandas as pd
from Scan import Scan as scan

import yfinance as yf
from Data7 import Data as data
import datetime
from Plot import Plot as plot


setups = pd.read_feather('C:/Screener/setups/EP.feather')
print(setups[setups['setup'] == 1])