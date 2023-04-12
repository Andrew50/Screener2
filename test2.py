




from tvDatafeed import TvDatafeed, Interval
from Scan import Scan as scan
import datetime
from pyarrow import feather
import pandas as pd
from Data7 import Data as data



#df = pd.DataFrame()


#df.to_feather("C:/Screener/tmp/screener_data.feather")
df = pd.read_feather("C:/Screener/tmp/setups.feather")


print(df)
