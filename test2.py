
from Data5 import Data as data
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import os
import datetime
from IntradayDatabase2 import Data

import datetime



df = data.get("COIN",'15min')


date = datetime.date(2023, 2, 9)


index = data.findex(df,date)

print(index)

