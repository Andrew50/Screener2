import pandas as pd
import datetime
from tvDatafeed import TvDatafeed
import os 
import datetime
import concurrent.futures
from Screen import Screen as screen
from functools import partial
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool
import warnings
warnings.filterwarnings("ignore")
class Data:
    def findIndex(df, dateTo):
        #this function essentialy takes in a dataframe and a date, and returns the index of the date in the dataframe. 
        # if the date is not contained in the dataframe, it returns 99999
        for i in range(len(df)):
            dateTimeOfDay = df.index[i]
            dateSplit = str(dateTimeOfDay).split(" ")
            date = dateSplit[0]
            if(date == dateTo):
                return i

        return 99999
    def isMarketClosed():
        #function returns a boolean based on whether or not the market is closed. If market is open, returns false. If market is closed, returns True
        dayOfWeek = datetime.datetime.now().weekday()
        if(dayOfWeek == 5 or dayOfWeek == 6): # datetime.now().weekday() returns a value 0-6 depending on the weekday, 0 if monday, 6 if sunday. Checks If Saturday/Sunday
            return True
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        # captures the main chunk of market hour sessions between 6am - 11:59 am 
        if(hour > 5 and hour < 24):
            return False
        # market doesn't open until 5:30 am, has to check if its at least 5:30
        elif(hour == 5):
            if(minute >= 30):
                return False
        elif(hour == 12):
            if(minute <= 15): #giving a 15 minute buffer if data is delayed due to not using paid acc, treats it as if markets open until 12:15 pm 
                return False
        else: 
            return True
        
    def updateTicker(exchangeTicker):

        
        split = exchangeTicker.split(":")
        exchange = split[0]
        ticker = split[1]
        isClosed = split[2]
        numLeft = split[3]
        lastDStock = split[4]
        try:
            # If there is no file for the current ticker that the code is iterating on, request the last 3500 bars and make a file
            if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv") == False):
                tv = TvDatafeed()
                data_daily = tv.get_hist(ticker, exchange, n_bars=3500)
                
                if isClosed == "False":
                    
                    data_daily.drop(data_daily.tail(1).index,inplace=True)
                    
                data_daily.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                #print(f"{ticker} created. Remaining: {numLeft}")
                message = str(f"{ticker} created")
                #prints.sendmessage(prints,message)
                print(message)

            # if there is a file, we now are going to check if the data is complete
            else:
                # read in the ticker's file
                cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                lastDayTime = cs.iloc[len(cs)-1]['datetime']
                lastDaySplit = lastDayTime.split(" ")
                lastDay = lastDaySplit[0]
                if (lastDay != lastDStock):
                    tv = TvDatafeed()
                    cs['datetime'] = pd.to_datetime(cs['datetime'])
                    cs = cs.set_index('datetime')
                    data_daily = tv.get_hist(ticker, exchange, n_bars=3500)
                    scrapped_data_index = Data.findIndex(data_daily, lastDay)
                    if(isClosed == "False"):
                        data_daily = data_daily.drop(index=data_daily.index[-1])
                    need_append_data = data_daily[scrapped_data_index+1:]
                    #print(need_append_data.head())
                    cs = pd.concat([cs, need_append_data])
                    cs.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                    numRows = len(need_append_data)
                    message = str(f"{ticker} appended with {numRows}")
                    print(message)
                    #prints.sendmessage(prints,message)
                    #print(f"{ticker} appended with {numRows}. Remaining: {numLeft}")
                else:
                    message = str(f"{ticker} approved")
                    print(message)
                    #prints.sendmessage(prints,message)
                    #print(f"{ticker} approved. Remaining: {numLeft}")
        except TimeoutError:
            print(ticker + " timed out")
        except OSError:
            print(ticker + " couldn't save file")
        except UnboundLocalError:
            print(ticker + " had issues !!!!!!!!!!!!!")

    


    def isDataUpdated(tv):
        # Takes in some dataframe that was given to the function and renames it 
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        numTickers = len(screener_data) #Number of Tickers contained in the dataframe
        #Grabs the last two sessions of apple. 
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        isClosed = Data.isMarketClosed()
        last = 't' # placeholder variables for future use since variable values are created in a if statement
        lastDStock = 't' #placeholder
        # if the market is closed, its free to access the most recent day since the data is complete. This code basically finds the most recent trading day
        if(isClosed == True):
            last = data_apple.index[1]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        # if the market is open, we should only use data from session prior to the most recent that is listed in the data. So, it takes the date for trading day T minus 1 
        elif(isClosed == False):
            last = data_apple.index[0]
            lastSplit = str(last).split(" ")
            lastDStock = lastSplit[0]
        print(lastDStock)
        tickers = []
        for i in range(numTickers):

            if str(screener_data.iloc[i]['Exchange']) == "NYSE ARCA":
                screener_data.at[i, 'Exchange'] = "AMEX"
            ticker = screener_data.iloc[i]['Ticker']
            exchange = screener_data.iloc[i]['Exchange']
            numTickersLeft = (numTickers - 1) - i
            closed = str(isClosed)

            tickers.append(f'{exchange}:{ticker}:{closed}:{numTickersLeft}:{lastDStock}')
        tickersLength = len(tickers)

        pool = Pool(nodes=8)
        pool.map(Data.updateTicker, tickers)
        #with concurrent.futures.ProcessPoolExecutor() as executor:


          #  ticks = tickers
          #  results = {executor.submit(Data.updateTicker, tick, repeat(tradView)) for tick in ticks}
          #  for result in results:
          #      print(result.result())
            #executor.map(Data.updateTicker, ticks, repeat(tradView))
            #for f in concurrent.futures.as_completed(resul)

        return 'done'

if __name__ == '__main__':
    tv = TvDatafeed()
    print(datetime.datetime.now()) 
    Data.isDataUpdated(tv)
    print(datetime.datetime.now())



class prints:

    def __init__(self):
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        numTickers = len(screener_data)
        self.remaining = numTickers

    def sendmessage(self,message):
        self.remaining -= 1
        print(f"message : {self.remaining}")