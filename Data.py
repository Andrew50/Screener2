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
from datetime import datetime, timedelta
class Data:
    def findIndex(self,df, dateTo):
        for i in range(len(df)):
            dateTimeOfDay = df.index[i]
            dateSplit = str(dateTimeOfDay).split(" ")
            date = dateSplit[0]
            if(date == dateTo):
                return i

        return 99999
    def isDataUpdated(self):
        df = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        screener_data = df
        numTickers = len(screener_data)
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=1)
        index = len(data_apple) - 1
        if datetime.now().hour > 12:
            last = data_apple.index[index]
        else:
            last = data_apple.index[index - 1]
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
                    print(f"{ticker} created {i}")
                    
                else:
                    cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                    lastDayTime = cs.iloc[len(cs)-1]['datetime']
                    lastDaySplit = lastDayTime.split(" ")
                    lastDay = lastDaySplit[0]
          
                    if (lastDay != lastDStock):
                        print(lastDStock)
                        print(lastDay)
                        lastDStockval = datetime.strptime(lastDStock, '%Y-%m-%d')
                        lastDayval = datetime.strptime(lastDay, '%Y-%m-%d')

                        requireddays =(lastDStockval - lastDayval).days
                        df2 = tv.get_hist(ticker, exchange, n_bars=requireddays)

                        
                        df1 = pd.read_csv(f"C:/Screener/data_csvs/{ticker}_data.csv")
                        cs = pd.concat([df1, df2])
                        cs.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                        
                        print(f"{ticker} appended with {requireddays} {i}")


                        #cs['datetime'] = pd.to_datetime(cs['datetime'])
                       # cs = cs.set_index('datetime')
                        #data_daily = tv.get_hist(ticker, exchange, n_bars=3500)
                      #  scrapped_data_index = (data_daily, lastDay)
                     #   need_append_data = data_daily[scrapped_data_index+1:]
                     #   print(need_append_data.head())
                    #    cs = pd.concat([cs, need_append_data])
                      #  cs.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                     #   numRows = len(need_append_data)
                      #  print(f"{ticker} appended with {numRows} {i}")
                    else:
                        print(f"{ticker} approved {i}")
            except TimeoutError:
                print(ticker + " timed out")
            except RuntimeError:
                print(ticker + " timed out2")
Data.isDataUpdated(Data)


