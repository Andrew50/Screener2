

from Data6 import Data as data
from tvDatafeed import TvDatafeed, Interval
from Scan import Scan as scan




#tvr = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
#df = tvr.get_hist("AAPL", "NASDAQ", interval=Interval.in_1_minute, n_bars=1000)


#df.drop('symbol', axis = 1, inplace = True)
#df.reset_index(inplace = True)



df = data.get('SI','1min','0')
print(df)

#df = data.get('AAPL','5min','0')


#print(df.iloc[data.findex(df,date)][0])



