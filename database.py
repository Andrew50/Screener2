
from tvDatafeed import TvDatafeed
from Daily import Daily as daily


length = 100

tv = TvDatafeed()
data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=length)
print(data_apple)
for i in range(length-20):
    date = data_apple.iloc[i]['Datetime']
    print(date)


