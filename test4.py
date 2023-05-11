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


df = pd.read_csv(r"F:/Screener/logss.csv")

df.to_feather("C:/Screener/tmp/log.feather")