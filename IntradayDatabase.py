import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
import os 
import datetime
import concurrent.futures
from Screen import Screen as screen
from functools import partial
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool
import warnings
import math
import yfinance as yf
warnings.filterwarnings("ignore")


class Data:
    def findIndex(df, dateTo, fromdata):
        try:
            if dateTo == "0":
                return len(df)
            if not fromdata:
                df = df.set_index('Date')

        
            lookforSplit = dateTo.split("-")
            middle = int(len(df)/2)
            middleDTOD = str(df.index[middle])
            middleSplit = middleDTOD.split("-")  
            yearDifference = int(middleSplit[0]) - int(lookforSplit[0])
            monthDifference = int(middleSplit[1]) - int(lookforSplit[1])
            if(monthDifference < 0):
                yearDifference = yearDifference + 1
                monthDifference = -12 + monthDifference
            addInt = (yearDifference*-252) + (monthDifference*-21)
            newRef = middle + addInt

            if fromdata and not '00:00:00' in dateTo:
                dateTo = dateTo + " 00:00:00"
            if(newRef < 0):
                return 99999
            if( ((len(df) - newRef) < 20) or (newRef > len(df))):
            
                for i in range(35):
                
                    dateTimeofDayAhead = str(df.index[len(df)-35 + i])
                    if(dateTimeofDayAhead == dateTo):
                        return int(len(df) - 35 + i)
            else:
                for i in range(35):
                    dateTimeofDayBehind = str(df.index[newRef - i])
                    if(dateTimeofDayBehind == dateTo):
                        return (newRef - i)
                    dateTimeofDayAhead = str(df.index[newRef + i])
                    if(dateTimeofDayAhead == dateTo):
                        return (newRef + i)
            return 99999
        except IndexError:
            print("findindex index error")
            return 99999
           
    def isMarketClosed():
        dayOfWeek = datetime.datetime.now().weekday()
        if(dayOfWeek == 5 or dayOfWeek == 6):
            return True
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        if(hour > 5 and hour < 12):
            return False
        elif(hour == 5):
            if(minute >= 30):
                return False
        elif(hour == 12):
            if(minute <= 15): 
                return False
        else: 
            return True
    def updatTick(tickersString):

        tickers = tickersString.split(' ')
        try:
        
            for t in tickers:
                tick = t.split(":")[0]
                exchange = t.split(":")[1]
                print(f"{tick} {exchange}")
                tv = TvDatafeed(username="cs.benliu@gmail.com", password="tltShort!1")
                ticker_df = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=10000)
                print(ticker_df)
                if(os.path.exists("C:/Screener/intraday_data/" + tick + "_intradaydata.csv") == False):
                    ticker_df.to_csv("C:/Screener/intraday_data/" + tick + "_intradaydata.csv")
                    print(f"{tick} created")
                else:
                    cs = pd.read_csv(r"C:/Screener/intraday_data/" + tick + "_intradaydata.csv")
                    lastDay = cs.iloc[len(cs)-1]['datetime']
                    cs['datetime'] = pd.to_datetime(cs['datetime'])
                    cs = cs.set_index('datetime')
                    scrapped_data_index = Data.findIndex(ticker_df, lastDay,True) 
                    
                    need_append_data = ticker_df[scrapped_data_index + 1:]
                    
                    cs = pd.concat([cs, need_append_data])
                    cs.to_csv("C:/Screener/intraday_data/" + ticker + "_intradaydata.csv")
                    numRows = len(need_append_data)
                    print(f"{tick} appended with {numRows}")
                
        except KeyError:
            print("had issue with KeyError")
        except TypeError:
            pass
        except OSError:
            print("os error")
        except IndexError:
            print("index error")



    def isTickerUpdated(tickerandDate):
        ticker = tickerandDate.split(":")[0]
        lastDStock = tickerandDate.split(":")[1]
        exchange = tickerandDate.split(":")[2]
        if(os.path.exists("C:/Screener/intraday_data/" + ticker + "_intradaydata.csv") == False):
            s = f"{ticker}:{exchange}"
            return s
        else:
            
            cs = pd.read_csv(r"C:/Screener/intraday_data/" + ticker + "_intradaydata.csv")
            if len(cs) > 1:
                lastDayTime = cs.iloc[len(cs)-1]['datetime']
                lastDaySplit = lastDayTime.split(" ")
                lastDay = lastDaySplit[0]
   
          
                if (lastDay != lastDStock):
               
                    s = f"{ticker}:{exchange}"
                    return s
                print(f"{ticker} is approved")
            else:
                print(f"{ticker} too young")
    

   
    def runUpdate(tv,allTickers):
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        isClosed = Data.isMarketClosed()
       
        last = 't' 
        lastDStock = 't' 
        if(isClosed == True):
            last = data_apple.index[1]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        elif(isClosed == False):
            last = data_apple.index[0]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        if allTickers:
            screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
        else:
            screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        numTickers = len(screener_data)
        tickers = []
        for i in range(numTickers):
           ticker = screener_data.iloc[i]['Ticker']
           exchange = screener_data.iloc[i]['Exchange']
           if(exchange == "NYSE ARCA"):
               exchange = "AMEX"
           tickers.append(f'{ticker}:{lastDStock}:{exchange}')
        remaining_tickers = []
        with Pool(nodes=3) as pool:
            remaining_tickers = pool.map(Data.isTickerUpdated, tickers)
        new_remaining = []
        for t in remaining_tickers:
            if(t != None):
                new_remaining.append(t)
        numLeft = len(new_remaining)
        print(numLeft)
        numIterations = math.ceil(float(numLeft/50))
        tickerBatches = []
        for i in range(numIterations):
            tickerString = ""
            if(i < numIterations-1):
                for j in range(50):
                    num = (i*50)+j
                    tickerString = tickerString + new_remaining[num] + " "
            else:
                for j in range(numLeft - (50*(i)) ):
                    num = (i*50)+j
                    tickerString = tickerString + new_remaining[num] + " "
            tickerBatches.append(tickerString)
        with Pool(nodes=5) as pool:
            pool.map(Data.updatTick, tickerBatches)

  

if __name__ == '__main__':
    tv = TvDatafeed()
    Data.runUpdate(tv,True)
    




