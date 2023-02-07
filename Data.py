from tkinter import N
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
from discordwebhook import Discord
import statistics
import mplfinance as mpf
import matplotlib as mpl
import pathlib
import math
import os 
class Data:
    def findIndex(df, dateTo):
        for i in range(len(df)):
            dateTimeOfDay = df.index[i]
            dateSplit = str(dateTimeOfDay).split(" ")
            date = dateSplit[0]
            if(date == dateTo):
                return i

        return 99999
    def isMarketClosed():
        dayOfWeek = datetime.datetime.now().weekday()
        if(dayOfWeek == 5 or dayOfWeek == 6): #If Saturday/Sunday
            return True
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        if(hour > 6 and hour < 12):
            return False

        elif(hour == 5):
            if(minute >= 30):
                return False
        elif(hour == 12):
            if(minute <= 15): #giving a 15 minute buffer if data is delayed due to not using paid acc
                return False
        else: 
            return True
        

    def isDataUpdated(self, df):
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        screener_data = df
        numTickers = len(screener_data)
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        isClosed = self.isMarketClosed()
        last = 't' # placeholder
        lastDStock = 't' #placeholder
        
        if(isClosed == True):
            last = data_apple.index[1]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        elif(isClosed == False):
            last = data_apple.index[0]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        for i in range(numTickers):

            if str(screener_data.iloc[i]['Exchange']) == "NYSE ARCA":
                screener_data.at[i, 'Exchange'] = "AMEX"
        for i in range(numTickers):
            ticker = screener_data.iloc[i]['Ticker']
            exchange = screener_data.iloc[i]['Exchange']
            try:
                if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv") == False):
                    data_daily = tv.get_hist(ticker, exchange, n_bars=3500)
                    data_daily.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                    print(f"{ticker} created #{i}")
        
                else:
                    cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                    lastDayTime = cs.iloc[len(cs)-1]['datetime']
                    lastDaySplit = lastDayTime.split(" ")
                    lastDay = lastDaySplit[0]
                    if (lastDay != lastDStock):
                        cs['datetime'] = pd.to_datetime(cs['datetime'])
                        cs = cs.set_index('datetime')
                        data_daily = tv.get_hist(ticker, exchange, n_bars=3500)
                        scrapped_data_index = self.findIndex(data_daily, lastDay)
                        if(isClosed == False):
                            data_daily = data_daily.drop(index=data_daily.index[-1])
                        need_append_data = data_daily[scrapped_data_index+1:]
                        print(need_append_data.head())
                        cs = pd.concat([cs, need_append_data])
                        cs.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                        numRows = len(need_append_data)
                        print(f"{ticker} appended with {numRows} #{i}")
                    else:
                        print(f"{ticker} approved #{i}")
            except TimeoutError:
                print(ticker + " timed out")


        return 'done'

screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
print(Data.isMarketClosed())
Data.isDataUpdated(Data, screener_data)






