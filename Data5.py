
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
import os 
import datetime
from pathos.multiprocessing import ProcessingPool as Pool
import warnings
import math
import yfinance as yf

warnings.filterwarnings("ignore")

class Data:
    def findex(df,datetime):

        #print(df)
        for i in range(len(df)):
            #print(f"{datetime} , {df.index[i]}")
            if datetime < df.index[i]:
                return i - 1 
        
        

    def get(ticker,interval):
        if interval == 'd' or interval == 'w' or interval == 'm':
            df = pd.read_csv(r"C:/Screener/daily_data/" + ticker + ".csv")
        else:
            df = pd.read_csv(r"C:/Screener/minute_data/" + ticker + ".csv")

        #df['index1'] = df.index
        
        df['datetime'] = pd.to_datetime(df['datetime'])
        if interval != 'd' and interval != '1min':
            df = df.set_index('datetime')
            logic = {'open'  : 'first',
                        'high'  : 'max',
                        'low'   : 'min',
                        'close' : 'last',
                        'volume': 'sum'
                        #,'index1': 'first'
                        }
        
            df = df.resample(interval).apply(logic)
            df.dropna(inplace = True)
            #df.index = df.index - pd.tseries.frequencies.to_offset("6D")
            df = df.reset_index()    
      

        return (df)

    

    def updatTick(tickersString):

        tickers = tickersString.split(' ')
       
        test = yf.download(tickers =  tickersString,  
            period = "25y",  group_by='ticker',      
            interval = "1d",      
            ignore_tz = True,     
            prepost = False) 
        
       
        for ticker in tickers:
            break
            try:
                ticker_df = test[ticker]
                ticker_df = ticker_df.drop(axis=1, labels="Adj Close")

                for i in range(len(ticker_df)):                 
                    if(math.isnan(ticker_df.iloc[i]['Close']) == False):
                        ticker_df = ticker_df[i:]
                        break


                ticker_df['datetime'] = pd.to_datetime(ticker_df.index)
                ticker_df = ticker_df.set_index('datetime')
                ticker_df.rename(columns={'Open':'open', 'High':'high', 'Low':'low','Close':'close','Volume':'volume'}, inplace = True)
                ticker_df.dropna(inplace = True)
                if(os.path.exists("C:/Screener/daily_data/" + ticker + ".csv") == False):
                    if not Data.isMarketClosed():
                        ticker_df.drop(ticker_df.tail(1).index,inplace=True)

                    #print(ticker_df)
                    ticker_df.to_csv("C:/Screener/daily_data/" + ticker + ".csv")
                    print(f"created {ticker} daily")
                else:
                    cs = pd.read_csv(r"C:/Screener/daily_data/" + ticker + ".csv")
                    cs['datetime'] = pd.to_datetime(cs['datetime'])
                    lastDay = cs.iloc[len(cs)-1]['datetime']
                
                    cs = cs.set_index('datetime')
                
                    scrapped_data_index = Data.findex(ticker_df, lastDay) 
                    if scrapped_data_index != None:
                    #print(scrapped_data_index)
                        need_append_data = ticker_df[scrapped_data_index + 1:]
                    
                        cs = pd.concat([cs, need_append_data])
                        cs.to_csv("C:/Screener/daily_data/" + ticker + ".csv")
                        numRows = len(need_append_data)
                
                        if numRows == 0:
                            print(f"deleted {ticker} daily")
                            os.remove(r"C:/Screener/daily_data/" + ticker + ".csv")
                        else:
                            print(f"appended {numRows} to {ticker} daily")
                    else:
                        print(f"failed {ticker} daily")
            except TypeError:
                print(f"failed {ticker} daily")
        test = yf.download(tickers =  tickersString,  
        period = "5d",  group_by='ticker',      
        interval = "1m",      

        ignore_tz = True,
            prepost = False) 
        for ticker in tickers:
            try:
                ticker_df = test[ticker]
                ticker_df = ticker_df.drop(axis=1, labels="Adj Close")
                ticker_df.dropna(inplace = True)
                if ((datetime.datetime.now().hour >= 5 and datetime.datetime.now().minute >= 30) or (datetime.datetime.now().hour >= 6)) and datetime.datetime.now().hour <= 12:
                    ticker_df.drop(ticker_df.tail(1).index,inplace=True)
                
                if(os.path.exists("C:/Screener/minute_data/" + ticker + ".csv") == False):
                    ticker_df.to_csv("C:/Screener/minute_data/" + ticker + ".csv")
                    print(f"created {ticker} minunte")
                else:
                    cs = pd.read_csv(r"C:/Screener/minute_data/" + ticker + ".csv")
                    

                    cs['datetime'] = pd.to_datetime(cs['datetime'])
                    lastDay = cs.iloc[len(cs)-1]['datetime']
                    cs = cs.set_index('datetime')
                    scrapped_data_index = Data.findex(ticker_df, lastDay) 
                    
                    if scrapped_data_index != None:
                        need_append_data = ticker_df[scrapped_data_index + 1:]
                    
                        cs = pd.concat([cs, need_append_data])
                        cs.to_csv("C:/Screener/minute_data/" + ticker + ".csv")
                        numRows = len(need_append_data)
                        print(f"appended {numRows} to {ticker} minute")
                    else:
                        print(f"failed {ticker} minute ")
        
            except TimeoutError:
                print(f"error {ticker} minute")
        


    def isTickerUpdated(tickerandDate):
        ticker = tickerandDate.split(":")[0]
        lastDStock = tickerandDate.split(":")[1]
        #exchange = tickerandDate.split(":")[2]
        if(os.path.exists("C:/Screener/daily_data/" + ticker + ".csv") == False):
            return ticker
        else:
            
            cs = pd.read_csv(r"C:/Screener/daily_data/" + ticker + ".csv")
           
            lastDay = cs.iloc[len(cs)-1]['datetime']
            #lastDaySplit = lastDayTime.split(" ")
            # lastDay = lastDaySplit[0]
   
            #print(f"{lastDay},{lastDStock}")
            if (lastDay != lastDStock):
                #print(f"{lastDay} , {lastDStock}")
                lastDay = datetime.datetime.strptime(lastDay, '%Y-%m-%d')
                lastDStock = datetime.datetime.strptime(lastDStock, '%Y-%m-%d')
                if lastDStock < lastDay:
                    print(f"deleted {ticker}")
                    os.remove(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                    #s = f"{ticker}:{exchange}"
                    return ticker
                else:
                    # s = f"{ticker}:{exchange}"
                    return ticker
            print(f"approved {ticker}")
           # except IndexError:
           #     print(f"deleted {ticker}")
             #   os.remove(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
           # except TimeoutError:
              #  print("value error in istickerupate")
    

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
    def runUpdate(tv):
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        isClosed = Data.isMarketClosed()
        if isClosed == None:
            isClosed = True
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
       
        screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
      
        numTickers = len(screener_data)
        tickers = []
        for i in range(numTickers):
           ticker = screener_data.iloc[i]['Ticker']
           #exchange = screener_data.iloc[i]['Exchange']
           #if(exchange == "NYSE ARCA"):
           #    exchange = "AMEX"
          # tickers.append(f'{ticker}:{lastDStock}:{exchange}')
           tickers.append(f'{ticker}:{lastDStock}')

           
        remaining_tickers = []
        
        with Pool(nodes=6) as pool:
            remaining_tickers = pool.map(Data.isTickerUpdated, tickers)
        new_remaining = []
        for t in remaining_tickers:
            if(t != None) and t != '':
                new_remaining.append(t)
        numLeft = len(new_remaining)
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
        #print(tickerBatches)
        with Pool(nodes=2) as pool:
            pool.map(Data.updatTick, tickerBatches)

  

if __name__ == '__main__':
    tv = TvDatafeed()
    Data.runUpdate(tv)
    




