


from ast import Mult, Num
import numpy
from tqdm import tqdm
import pandas as pd
import datetime
import sys
import numpy as np
from tvDatafeed import TvDatafeed, Interval
import os 
import datetime
#from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing  import Pool
import warnings
import math
import yfinance as yf
warnings.filterwarnings("ignore")



class Data:

    def pool(deff,arg,nodes = 7):
            pool = Pool(processes = nodes)
            data = list(tqdm(pool.imap(deff, arg), total=len(arg)))
            return(data)

    def isToday(dt):
        if dt == None:
            return False
        if dt == 'Today' or dt == '0' or dt == 0:
            return True
        time = datetime.time(0,0,0)
        today = datetime.date.today()
        today = datetime.datetime.combine(today,time)
        if type(dt) is str:
            try:
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
            except:
                    
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        if type(dt) is datetime.date:
            time = datetime.time(0,0,0)
            dt = datetime.datetime.combine(dt,time)
        if dt >= today:
            return True

        return False

    def findex(df,dt):
        try:
            if Data.isToday(dt):
                return len(df) - 1
            if type(dt) == str:
                try:
                    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                except:
                    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

            if type(dt) == datetime.date:
                time = datetime.time(9,30,0)
                dt = datetime.datetime.combine(dt,time)
            if dt.time() == datetime.time(0):
                time = datetime.time(9,30,0)
                dt = datetime.datetime.combine(dt.date(),time)
            i = int(len(df)/2)
            k = i
            while True:
                k = int(k/2)
                date = df.iloc[i]['datetime'].to_pydatetime()
                if date > dt:
                    i -= k
                elif date < dt:
                    i += k
                if k == 0:
                    break
            while True:
                if df.iloc[i]['datetime'].to_pydatetime() < dt:
                    i += 1
                else:
                    break
            while True:
                if df.iloc[i]['datetime'].to_pydatetime() > dt:
                    i -= 1
                else:
                    break
            return i
        except TimeoutError:
            return None

    def get(ticker,tf = 'd',date = None,premarket = False):
        current = Data.isToday(date)
        if tf == 'd' or tf == 'w' or tf == 'm':
            df = pd.read_csv(r"C:/Screener/daily_data/" + ticker + ".csv")
            df['datetime'] = pd.to_datetime(df.iloc[:,0])
            df = df.set_index('datetime')
        else:
            if current:
                tvr = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
                screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
                screener_data.set_index('Ticker', inplace = True)
                exchange = str(screener_data.loc[ticker]['Exchange'])
                df = tvr.get_hist(ticker, exchange, interval=Interval.in_1_minute, n_bars=1000, extended_session = premarket)
                df.drop('symbol', axis = 1, inplace = True)
                df.index = df.index + pd.Timedelta(hours=4)



                seconds = datetime.datetime.now().second
                

                bar = df.iloc[-1]
                df.drop(df.tail(1).index,inplace = True)

                if seconds > 20:

                
                    mult = pow((60 / seconds),.75)

                    openn = bar['open']
                    high = bar['high']
                    low = bar['low']
                    close = bar['close']
                    vol = bar['volume']

                    new_open = openn
                    new_close = close + (close - openn) * mult 
                    new_vol = vol*mult 
                    new_high = high
                    new_low = low

                    if new_close > high:
                        new_high = new_close
                    if new_close < low:
                        new_low = new_close
                

                    new = pd.DataFrame({'datetime':[datetime.datetime.now()],
                                        'open':[new_open],
                                        'high':[new_high],
                                        'low':[new_low],
                                        'close':[new_close],
                                        'volume':[new_vol]})

                    new = new.set_index('datetime')
                    df = pd.concat([df,new])



            else:
                df = pd.read_csv(r"C:/Screener/minute_data/" + ticker + ".csv")
                df['datetime'] = pd.to_datetime(df.iloc[:,0])
                df = df.set_index('datetime')
                if not premarket:
                    df = df.between_time('09:30' , '15:59')
        if tf != 'd' and tf != '1min':
            logic = {'open'  : 'first',
                        'high'  : 'max',
                        'low'   : 'min',
                        'close' : 'last',
                        'volume': 'sum' }
            df = df.resample(tf).apply(logic)
        df.dropna(inplace = True)
        df = df.reset_index()
        if current and (tf == 'd' or tf == 'w' or tf == 'm'):
            screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
            screener_data.set_index('Ticker', inplace = True)
            screenbar = screener_data.loc[ticker]
            pm = screenbar['Price'] + screenbar['Pre-market Change']
            date = np.datetime64(datetime.date.today())
            row  ={'datetime': [date],
                   'open': [pm],
                   'high': [pm],
                   'low': [pm],
                   'close': [pm],
                   'volume': [0]}
            row = pd.DataFrame(row)
            df = pd.concat([df, row])
            df = df.reset_index()
            df.drop('index', axis = 1, inplace = True)
        return (df)
        
    def updatTick(ticker):
        test = yf.download(tickers =  ticker,  
            period = "25y",  group_by='ticker',      
            interval = "1d",      
            ignore_tz = True,  
            progress=False,
            show_errors = False,
            threads = False,
            prepost = False) 
        
        try:
            ticker_df = test
            ticker_df = ticker_df.drop(axis=1, labels="Adj Close")
            for i in range(len(ticker_df)):                 
                if(math.isnan(ticker_df.iloc[i]['Close']) == False):
                    ticker_df = ticker_df[i:]
                    break
            ticker_df['datetime'] = pd.to_datetime(ticker_df.index)
            ticker_df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'}, inplace = True)
            ticker_df.dropna(inplace = True)
            if(os.path.exists("C:/Screener/daily_data/" + ticker + ".csv") == False):
                if not Data.isMarketClosed():
                    ticker_df.drop(ticker_df.tail(1).index,inplace=True)
                ticker_df.drop('datetime', axis = 1, inplace = True)
                ticker_df.index.rename('datetime', inplace = True)
                ticker_df.to_csv("C:/Screener/daily_data/" + ticker + ".csv")
            else:
                cs = Data.get(ticker,'d') 
                lastDay = cs.iloc[len(cs)-1]['datetime'].date()
                cs = cs.set_index('datetime')
                scrapped_data_index = Data.findex(ticker_df, lastDay) 
                if scrapped_data_index != None:
                    ticker_df = ticker_df[scrapped_data_index + 1:]
                    ticker_df.drop('datetime', axis = 1, inplace = True)
                    cs = pd.concat([cs, ticker_df])
                    cs.index.rename('datetime', inplace = True)
                    cs.to_csv("C:/Screener/daily_data/" + ticker + ".csv")
                    numRows = len(ticker_df)
                    if numRows == 0:
                        os.remove(r"C:/Screener/daily_data/" + ticker + ".csv")
      
        except:
            pass

        if not (((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)) and (datetime.datetime.now().weekday() < 5)):   #if it is in the morning and u forgot to update data it ill just do daily
            test = yf.download(tickers =  ticker,  
            period = "5d",  group_by='ticker',      
            interval = "1m",      
            ignore_tz = True,
            threads = False,
            progress=False,
            show_errors = False,
            prepost = False) 
            try:
                ticker_df = test
                ticker_df = ticker_df.drop(axis=1, labels="Adj Close")
                ticker_df['datetime'] = pd.to_datetime(ticker_df.index)
                ticker_df.rename(columns={'Open':'open', 'High':'high', 'Low':'low','Close':'close','Volume':'volume'}, inplace = True)
                if (datetime.datetime.now().weekday() < 5) and ((datetime.datetime.now().hour >= 5 and datetime.datetime.now().minute >= 30) or (datetime.datetime.now().hour >= 6)) and datetime.datetime.now().hour <= 12:
                    ticker_df.drop(ticker_df.tail(1).index,inplace=True)
                if(os.path.exists("C:/Screener/minute_data/" + ticker + ".csv") == False):
                    ticker_df.dropna(inplace = True)
                    ticker_df.drop('datetime', axis = 1, inplace = True)
                    ticker_df.index.rename('datetime', inplace = True)
                    ticker_df.to_csv("C:/Screener/minute_data/" + ticker + ".csv")
                else:
                    cs = Data.get(ticker,'1min')
                    lastDay = cs.iloc[len(cs)-1]['datetime'].to_pydatetime()
                    cs = cs.set_index('datetime') 
                    scrapped_data_index = Data.findex(ticker_df, lastDay) 
                    if scrapped_data_index != None:
                        scrapped_data_index = scrapped_data_index + 1
                        if scrapped_data_index != len(ticker_df):
                            ticker_df = ticker_df[scrapped_data_index:]
                            ticker_df.dropna(inplace = True)
                            ticker_df.drop('datetime', axis = 1, inplace = True)
                            cs = pd.concat([cs, ticker_df])
                            cs.index.rename('datetime', inplace = True)
                            cs.to_csv("C:/Screener/minute_data/" + ticker + ".csv")
                            numRows = len(ticker_df)
            except:
                pass
 
    def isTickerUpdated(tickerandDate):
        ticker = tickerandDate.split(":")[0]
        lastDStock = tickerandDate.split(":")[1]
        if(os.path.exists("C:/Screener/daily_data/" + ticker + ".csv") == False):
            return ticker
        else:
            try:
                cs = Data.get(ticker)
                lastDay = cs.iloc[len(cs)-1]['datetime'].to_pydatetime()
                lastDStock = datetime.datetime.strptime(lastDStock, '%Y-%m-%d')
                if (lastDay != lastDStock):
                    return ticker
            except:
                pass

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
    def runUpdate():
        tv = TvDatafeed()
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

        #screener_data = pd.DataFrame({'Ticker': ['COIN', 'HOOD'],
       #                               'Exchange':['NASDAQ' , 'NASDAQ']})
        
        numTickers = len(screener_data)
        tickers = []
        for i in range(numTickers):
           ticker = screener_data.iloc[i]['Ticker']
           tickers.append(f'{ticker}:{lastDStock}')
        remaining_tickers = []
        print('scanning')
        remaining_tickers = Data.pool(Data.isTickerUpdated, tickers)
        new_remaining = []
        for t in remaining_tickers:
            if(t != None) and t != '':
                new_remaining.append(t)
        numLeft = len(new_remaining)
        numIterations = math.ceil(float(numLeft/50))
        batchsize = 20
        tickerBatches = []
        print('pulling')
        Data.pool(Data.updatTick, new_remaining)

if __name__ == '__main__':
    Data.runUpdate()
    





