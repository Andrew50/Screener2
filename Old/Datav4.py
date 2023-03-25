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
    def findWeeklyIndex(df,index):
        k = 0
        while k < 10:
            try:
                value = df.loc[index - k]['index2']
                return value
            except:
                k += 1
        return 9999
    def toWeekly(data_daily):
      
        #save the daily datas index into a column for later
        data_daily['index1'] = data_daily.index
        #convert the string thing or whatever to a datetime object
        data_daily['Datetime'] = pd.to_datetime(data_daily['Date'])
        #set the index as that datetime object
        df = data_daily.set_index('Datetime')
        logic = {'Open'  : 'first',
                 'High'  : 'max',
                 'Low'   : 'min',
                 'Close' : 'last',
                 'Volume': 'sum',
                 'index1': 'first'}

        #convert to weekly
        dfw = df.resample('W').apply(logic)
        dfw.index = dfw.index - pd.tseries.frequencies.to_offset("6D")
        dfw = dfw.reset_index()    
        dfw['index2'] = dfw.index
        #sets the index to the first days index in that week so that findIndex can be done easily
        dfw = dfw.set_index('index1')
      

        return (dfw)

    

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
                        try:
                            dateTimeofDayBehind = str(df.index[newRef - i])
                            if(dateTimeofDayBehind == dateTo):
                                return (newRef - i)
                            dateTimeofDayAhead = str(df.index[newRef + i])
                            if(dateTimeofDayAhead == dateTo):
                                return (newRef + i)
                        except IndexError:
                            pass
                
            #print(str(f"{dateTimeofDayAhead} , {dateTo}"))
            
            return 99999
        except:
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
        test = yf.download(tickers =  tickersString,  
            period = "25y",  group_by='ticker',      
            interval = "1d",      
            ignore_tz = True,     
            prepost = False) 
        try:
        
            for ticker in tickers:
                ticker_df = test[ticker]
                ticker_df = ticker_df.drop(axis=1, labels="Adj Close")

                for i in range(len(ticker_df)):                 
                    if(math.isnan(ticker_df.iloc[i]['Close']) == False):
                        ticker_df = ticker_df[i:]
                        break
                if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv") == False):
                    if not Data.isMarketClosed():
                        ticker_df.drop(ticker_df.tail(1).index,inplace=True)
                    ticker_df.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                    print(f"created {ticker}")
                else:
                    cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                    lastDay = cs.iloc[len(cs)-1]['Date']
                    cs['Date'] = pd.to_datetime(cs['Date'])
                    cs = cs.set_index('Date')
                    scrapped_data_index = Data.findIndex(ticker_df, lastDay,True) 
                    #print(scrapped_data_index)
                    need_append_data = ticker_df[scrapped_data_index + 1:]
                    
                    cs = pd.concat([cs, need_append_data])
                    cs.to_csv("C:/Screener/data_csvs/" + ticker + "_data.csv")
                    numRows = len(need_append_data)
                    print(f"appended {numRows} to {ticker}")
                    if numRows == 0:
                        print(f"deleted {ticker}")
                        os.remove(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                
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
        if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv") == False):
            return ticker
        else:
            
            cs = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
            try:
                lastDayTime = cs.iloc[len(cs)-1]['Date']
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
        if allTickers:
            screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
        else:
            screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
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
    



