


from pyarrow import feather
from tqdm import tqdm
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
import os 
import datetime
import numpy
from multiprocessing  import Pool
import warnings
import yfinance as yf
warnings.filterwarnings("ignore")
import Scan


class Data:
    path = ""
    if os.path.exists("F:/Screener/Ffile.txt"):
        path = "F:/Screener"
    else: 
        path = "C:/Screener"
    def pool(deff,arg,nodes = 7):
            pool = Pool(processes = nodes)
            data = list(tqdm(pool.imap(deff, arg), total=len(arg)))
            return(data)







    def convert_date(dt):
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
        return(dt)






    def isToday(dt):
        if dt == None:
            return False
        if dt == 'Today' or dt == '0' or dt == 0:
            return True
        time = datetime.time(0,0,0)
        today = datetime.date.today()
        today = datetime.datetime.combine(today,time)
        dt = Data.convert_date(dt)
        if dt >= today:
            return True
        return False



    

    def findex(df,dt):
        try:
            
            if Data.isToday(dt):
                return len(df) - 1
            dt = Data.convert_date(dt)
            i = int(len(df)/2)
            k = i
           
            while True:
                k = int(k/2)
                date = df.index[i].to_pydatetime()
                if date > dt:
                    i -= k
                elif date < dt:
                    i += k
                if k == 0:
                    break
                
            while True:
                if df.index[i].to_pydatetime() < dt:
                    i += 1
                else:
                    break
            while True:
                if df.index[i].to_pydatetime() > dt:
                    i -= 1
                else:
                    break
            return i
        except IndexError:
            if i == len(df):
                return i
            
            return None




    def get(ticker = 'AAPL',tf = 'd',date = None,premarket = False,account = False):    
        path = Data.path


        current = Data.isToday(date)

        if tf == 'daily':
            tf = 'd'
        if tf == 'minute':
            tf = '1min'

        if tf == 'd' or tf == 'w' or tf == 'm':
            df = feather.read_feather(r"" + path + "/daily/" + ticker + ".feather")
        else:
            if current and not (datetime.datetime.now().hour < 5 or (datetime.datetime.now().hour < 6 and datetime.datetime.now().minute < 30)):

                tvr = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
                screener_data = feather.read_feather(r"C:\Screener\sync\screener_data_intraday.feather")
                screener_data.set_index('Ticker', inplace = True)
                #print(screener_data)
                exchange = str(screener_data.loc[ticker]['Exchange'])
                df = tvr.get_hist(ticker, exchange, interval=Interval.in_1_minute, n_bars=1000, extended_session = premarket)
                df.drop('symbol', axis = 1, inplace = True)
                df.index = df.index + pd.Timedelta(hours=4)

                if not account:

                    seconds = datetime.datetime.now().second
                    bar = df.iloc[-1]
                    df.drop(df.tail(1).index,inplace = True)
                    if seconds > 30:
                        mult = pow((60 / seconds),.6)
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

                        now = datetime.datetime.now()
                        new = pd.DataFrame({'datetime':[now],
                                            'open':[new_open],
                                            'high':[new_high],
                                            'low':[new_low],
                                            'close':[new_close],
                                            'volume':[new_vol]}).set_index("datetime")
                        df = pd.concat([df,new])

                else:
                    #fetch fiole
                    dff = feather.read_feather(r"" + path + "/daily/" + ticker + ".feather")
                    lastday = dff.index[-1]
                    scrapped_data_index = Data.findex(df,lastday) 
                    if not scrapped_data_index == None:
                        pass
                        
                    else:
                        df = df[scrapped_data_index + 1:]
                        df = pd.concat([dff,df])

            else:
                df = feather.read_feather(r"" + path + "/minute/" + ticker + ".feather")
                if not premarket:
                    df = df.between_time('09:30' , '15:59')



        if tf != 'd' and tf != '1min':
            logic = {'open'  : 'first',
                        'high'  : 'max',
                        'low'   : 'min',
                        'close' : 'last',
                        'volume': 'sum' }
            df = df.resample(tf).apply(logic)
        if current and (datetime.datetime.now().hour < 5 or (datetime.datetime.now().hour < 6 and datetime.datetime.now().minute < 30)):

            screenbar = Scan.Scan.get('0','d').loc[ticker]
            pmchange =  screenbar['Pre-market Change']


            if numpy.isnan(pmchange):
                pmchange = 0
            #if type(pmchange) != int():
           #     pmchange = 0
                
          
            try:
                pm = df.iat[-1,3] + pmchange
                date = pd.Timestamp(datetime.datetime.today())
                row  =pd.DataFrame({'datetime': [date],
                       'open': [pm],
                       'high': [pm],
                       'low': [pm],
                       'close': [pm],
                       'volume': [0]}).set_index("datetime")
                df = pd.concat([df, row])
          
            except IndexError:
                pass
        df.dropna(inplace = True)
        return (df)
        
    def update(bar):
        path = Data.path
        try:
            ticker = bar[0]
            lastDStock = bar[1]
            tf = bar[2]

            if ticker == None or "/" in ticker  or '.' in ticker:
                return

            exists = True
            try:
                cs = Data.get(ticker,tf)
                lastDay = cs.index[-1]
                if (lastDay == lastDStock):
                    return
            
            except:
                exists = False
            if tf == 'daily':
                ytf = '1d'
                period = '25y'
            else:
                ytf = '1m'
                period = '5d'
        
            ydf = yf.download(tickers =  ticker,  
                period = period,  group_by='ticker',      
                interval = ytf,      
                ignore_tz = True,  
                progress=False,
                show_errors = False,
                threads = False,
                prepost = False) 
        
        
            ydf = ydf.drop(axis=1, labels="Adj Close")
            ydf.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'}, inplace = True)
            if Data.isMarketOpen() == 1 :
                ydf.drop(ydf.tail(1).index,inplace=True)
            ydf.dropna(inplace = True)
  
            if not exists:
                df = ydf
                print(f'created {ticker} {tf}')
            else:
 
                scrapped_data_index = Data.findex(ydf, lastDay) 
                if scrapped_data_index == None:
                    return
                ydf = ydf[scrapped_data_index + 1:]
                df = pd.concat([cs, ydf])

            df.index.rename('datetime', inplace = True)


            #testing function //////////
            #df.to_csv("C:/Screener/data_test/" + ticker + tf+".csv")
            feather.write_feather(df, path + "/"+tf+"/" + ticker + ".feather")
        except FileNotFoundError:
            pass
    
    def runUpdate():
        tv = TvDatafeed()
        daily = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        daily_last = daily.index[Data.isMarketOpen()]
        minute = tv.get_hist('AAPL', 'NASDAQ', n_bars=2, interval=Interval.in_1_minute, extended_session = False)
        minute_last = minute.index[Data.isMarketOpen()]

        screener_data = Scan.Scan.get()
        
        
        #screener_data = pd.DataFrame({'Ticker': ['^VIX']
                               #       }).set_index('Ticker')
        
        batches = []
        for i in range(len(screener_data)):
           ticker = screener_data.index[i]
           batches.append([ticker, daily_last, 'daily'])
           batches.append([ticker, minute_last, 'minute'])
        
        Data.pool(Data.update, batches)
        

    def isMarketOpen():
        dayOfWeek = datetime.datetime.now().weekday()
        if(dayOfWeek == 5 or dayOfWeek == 6):
            return 0
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        if(hour > 5 and hour < 12):
            return 1
        elif(hour == 5):
            if(minute >= 30):
                return 1
        elif(hour == 12):
            if(minute <= 15): 
                return 1
        else: 
            return 0



if __name__ == '__main__':
    
    Data.runUpdate()
    






