




from tvDatafeed import TvDatafeed, Interval
from Scan import Scan as scan
import datetime
from pyarrow import feather
import pandas as pd
from Data7 import Data as data





df = pd.read_feather("C:/Screener/tmp/todays_setups.feather")


print(df)
