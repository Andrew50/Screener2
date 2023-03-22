


from tvDatafeed import TvDatafeed, Interval





tvr = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
data_minute = tvr.get_hist("AAPL", "NASDAQ", interval=Interval.in_1_minute, n_bars=1000)

print(data_minute)