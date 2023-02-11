
from tvDatafeed import TvDatafeed
from Daily import Daily as daily



length = 30

tv = TvDatafeed()
data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=length)

for i in range(length-20):
    dateTimeOfDay = data_apple.index[i]
    dateSplit = str(dateTimeOfDay).split(" ")
    date = dateSplit[0]
    print(str(f"backtesting  {date}"))
          
    daily.runDaily(daily, date,True)


