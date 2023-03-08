
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed
import os 
import datetime
from pathos.multiprocessing import ProcessingPool as Pool
import warnings
import math
import yfinance as yf

warnings.filterwarnings("ignore")

class Data:
    def findex(df,datetime):
        for i in range(len(df)):
            if datetime <= df.iloc[i]['datetime']:
                return i - 1 
            print('god')
        

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
            ticker_df = test[ticker]
            ticker_df = ticker_df.drop(axis=1, labels="Adj Close")

            for i in range(len(ticker_df)):                 
                if(math.isnan(ticker_df.iloc[i]['Close']) == False):
                    ticker_df = ticker_df[i:]
                    break


            ticker_df['datetime'] = pd.to_datetime(ticker_df.index)
            ticker_df = ticker_df.set_index('datetime')
            ticker_df.rename(columns={'Open':'open', 'High':'high', 'Low':'low','Close':'close','Volume':'volume'}, inplace = True)
            if(os.path.exists("C:/Screener/daily_data/" + ticker + ".csv") == False):
                if not Data.isMarketClosed():
                    ticker_df.drop(ticker_df.tail(1).index,inplace=True)

                #print(ticker_df)
                ticker_df.to_csv("C:/Screener/daily_data/" + ticker + ".csv")
                print(f"created {ticker}")
            else:
                cs = pd.read_csv(r"C:/Screener/daily_data/" + ticker + ".csv")
                lastDay = cs.iloc[len(cs)-1]['datetime']
                cs['datetime'] = pd.to_datetime(cs['datetime'])
                cs = cs.set_index('datetime')
                scrapped_data_index = Data.findIndex(ticker_df, lastDay,True) 
                #print(scrapped_data_index)
                need_append_data = ticker_df[scrapped_data_index + 1:]
                    
                cs = pd.concat([cs, need_append_data])
                cs.to_csv("C:/Screener/data_csvs/" + ticker + ".csv")
                numRows = len(need_append_data)
                print(f"appended {numRows} to {ticker}")
                if numRows == 0:
                    print(f"deleted {ticker}")
                    os.remove(r"C:/Screener/data_csvs/" + ticker + ".csv")
                
        


    def isTickerUpdated(tickerandDate):
        ticker = tickerandDate.split(":")[0]
        lastDStock = tickerandDate.split(":")[1]
        if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv") == False):
            return ticker
        else:
            
            cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
            try:
                lastDayTime = cs.iloc[len(cs)-1]['datetime']
                lastDaySplit = lastDayTime.split(" ")
                lastDay = lastDaySplit[0]
   
                
                if (lastDay != lastDStock):
                    #print(f"{lastDay} , {lastDStock}")
                    lastDay = datetime.datetime.strptime(lastDay, '%Y-%m-%d')
                    lastDStock = datetime.datetime.strptime(lastDStock, '%Y-%m-%d')
                    if lastDStock < lastDay:
                        print(f"deleted {ticker}")
                        os.remove(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                        return ticker
                    else:
                    
                        return ticker
                print(f"approved {ticker}")
            except IndexError:
                print(f"deleted {ticker}")
                os.remove(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
            except ValueError:
                print("value error in istickerupate")
    

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
    def runUpdate(tv,allTickers):
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        isClosed = Data.isMarketClosed()
        if isClosed == None:
            isClosed = True
        last = 't' 
        lastDStock = 't' 
        #print(isClosed)
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
           #print(f'{ticker}:{lastDStock}')
           tickers.append(f'{ticker}:{lastDStock}')
        remaining_tickers = []
        
        with Pool(nodes=6) as pool:
            remaining_tickers = pool.map(Data.isTickerUpdated, tickers)
        new_remaining = []
        for t in remaining_tickers:
            if(t != None):
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
        with Pool(nodes=2) as pool:
            pool.map(Data.updatTick, tickerBatches)

  

if __name__ == '__main__':
    tv = TvDatafeed()
    Data.runUpdate(tv,True)
    




