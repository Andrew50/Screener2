




from tvDatafeed import TvDatafeed, Interval
from Scan import Scan as scan
import datetime
from pyarrow import feather
import pandas as pd
from Data7 import Data as data



#df = pd.DataFrame()


df = pd.read_feather("C:/Screener/tmp/setups.feather")

'''


df = pd.read_feather("C:/Screener/tmp/full_ticker_list.feather")['Ticker'].to_list()

for i in df:
    if i == 'GOOG':
        print('god')
print(len(df))



'''

print(df)