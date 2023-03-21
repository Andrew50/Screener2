


import os
import pandas as pd
import statistics
import time
import datetime
from datetime import date, timedelta
from Log2 import log as log
import warnings
from pathos.multiprocessing import ProcessingPool as Pool
from tvDatafeed import TvDatafeed
warnings.filterwarnings("ignore")
from Data5 import Data as data
from Screen import Screen as screen
from UI3 import UI as ui

from Detection1 import Detection as detection




class Backtest:


    

    

    def processTickers(screenbar):

        try:
            
            timeframe = str(screenbar['interval'])
            ticker = str(screenbar['Ticker'])
            test = (screenbar['test'])
            dateToSearch = screenbar['dateToSearch']
            #print(ticker)


            dolVol, adr = Backtest.requirements(ticker,dateToSearch)

            

            if dolVol > 10000000 and adr > 3.5:

                
                df = data.get(ticker,timeframe)
                currentday = data.findex(df,dateToSearch)
        
                detection.check(dolVol, adr,df, currentday,screenbar, test,timeframe )


        except FileNotFoundError: 
            print(f"{ticker} is delisted")
        except TimeoutError:
            print(f"{ticker} failed")

            
            
    def get_list(dateToSearch,ticker):

        full = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
        if ticker != None:
            
            screener_data  = full.iloc[str(ticker)]
        else:
            
                
            if(dateToSearch.weekday() >= 5):
                print("The date given is not a weekday.")
                return False
            screener_data = full

        return screener_data

    def run( timeframe = 'd',dateToSearch = None, ticker = None):

        if dateToSearch != None or ticker != None:
            test = True
            if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                os.remove("C:/Screener/data_csvs/todays_setups.csv")
            pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
        else:
            test = False



        if dateToSearch == None:

            try:
                df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                strdate = df.iloc[len(df)-1][0]
           
                startdate = datetime.datetime.strptime(strdate, '%Y-%m-%d')
                print(f"starting from {startdate}")
                time.sleep(3)
            except:
                startdate = date(2008, 1, 1)
                
            sample = data.get('AAPL',timeframe)
            index = data.findex(sample,startdate)

            while index < len(sample) - 50:

                search = sample.iloc[index][0]

                Backtest.pool(timeframe,search,ticker,test)

                index += 1

        else:

            Backtest.pool(timeframe,dateToSearch,ticker, test)
            


    def pool( timeframe,dateToSearch, ticker,test):




        screener_data = Backtest.get_list(dateToSearch,ticker)

        screenbars = []
        for i in range(len(screener_data)):
            screener_data.at[i, 'dateToSearch'] = dateToSearch
            screener_data.at[i, 'interval'] = timeframe
            screener_data.at[i, 'test'] = test
            screenbars.append(screener_data.iloc[i])

        with Pool(nodes=6) as pool:
            pool.map(Backtest.processTickers, screenbars)
        
    def requirements(ticker,date):
        try:
            df = data.get(ticker,'d')
            currentday = data.findex(df,date)
            if(currentday == None): 
                print('god')
                return 0, 0
            dolVol = []
            for i in range(5):
                dolVol.append(df.iloc[currentday-1-i][4]*df.iloc[currentday-1-i][5])
            dolVol = statistics.mean(dolVol)

       
                            
            adr= []
            for j in range(20): 
                high = df.iloc[currentday-j-1][2]
                low = df.iloc[currentday-j-1][3]
                val = (high/low - 1) * 100
                adr.append(val)
                        
            adr = statistics.mean(adr)  
       
            return dolVol, adr
        except:
            print('requirements failed')
            return 0 , 0
        
if __name__ == '__main__':
    

    dateToSearch = datetime.datetime(2023,3,15)

    Backtest.run(dateToSearch = dateToSearch)
    
        
        