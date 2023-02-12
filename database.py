
from tvDatafeed import TvDatafeed
from Daily2 import Daily as daily



start = 70 #

tv = TvDatafeed()
data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=start)

for i in range(start-20):
    dateTimeOfDay = data_apple.index[i]
    dateSplit = str(dateTimeOfDay).split(" ")
    date = dateSplit[0]
    print(str(f"backtesting  {date}"))
          
    daily.runDaily(daily, date)


