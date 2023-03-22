


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




class Daily:

    

    def processTickers(screenbar):

        try:
            
            timeframe = str(screenbar['interval'])
            ticker = str(screenbar['Ticker'])
            dateToSearch = screenbar['dateToSearch']
            print(ticker)
            dolVol, adr = Daily.requirements(ticker,dateToSearch)

            

            if dolVol > 10000000 and adr > 3.5:

                
                df = data.get(ticker,timeframe)
                currentday = data.findex(df,dateToSearch)
        
                

                if (dateToSearch == "0"):    
                   
                    pmPrice = df.iloc[currentday-1][4] + screenbar['Pre-market Change']
       
                else:
                    
                    pmPrice = df.iloc[currentday][1]

                sEP = True
                sMR = True
                sPivot = True
                sFlag = True
                dolVolFilter = 10000000

                if(dolVol > .2* dolVolFilter  and adr > 3.5 and sEP):
                    Daily.EP(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > .8 * dolVolFilter    and adr > 5 and sMR):
                    Daily.MR(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > 1* dolVolFilter   and adr > 3.5 and sPivot):
                    Daily.Pivot(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > .8 * dolVolFilter   and adr > 4 and sFlag):
                    Daily.Flag(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
        except FileNotFoundError: 
            print(f"{ticker} is delisted")
        except TimeoutError:
            print(f"{ticker} failed")

            
            
    def get_list(dateToSearch,ticker):

        
        if ticker != None:
            full = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
            screener_data  = full.iloc[str(ticker)]
        else:
            tv = TvDatafeed()
            if dateToSearch == "0":
            
                screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
                if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                    os.remove("C:/Screener/data_csvs/todays_setups.csv")
                pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
                
                screen.runDailyScan(None)
                #data.runUpdate()

            else:
                
                if(dateToSearch.weekday() >= 5):
                    print("The date given is not a weekday.")
                    return False
                screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")

            return screener_data

    def runDaily(dateToSearch = '0', interval = 'd',ticker = None):
        
        screener_data = Daily.get_list(dateToSearch,ticker)

        screenbars = []
        for i in range(len(screener_data)):
            screener_data.at[i, 'dateToSearch'] = dateToSearch
            screener_data.at[i, 'interval'] = interval
            screenbars.append(screener_data.iloc[i])

        with Pool(nodes=6) as pool:
            pool.map(Daily.processTickers, screenbars)
        
        if dateToSearch == "0":
            ui.loop(ui,True)

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
            return 0 , 0
        
if __name__ == '__main__':
    

    

    
    timeframe = '5min'
    premarket = False


    replace_setups = True



    #forecast //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if False or ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)) :
            Daily.runDaily()


    #backtest ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else:
            
        if replace_setups:
            if(os.path.exists("C:/Screener/data_csvs/setups.csv")):
                os.remove("C:/Screener/data_csvs/setups.csv")
            pd.DataFrame().to_csv(("C:/Screener/tmp/setups.csv"),  header=False)
        
        try:
            df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
            strdate = df.iloc[len(df)-1][0]
           
            startdate = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            print(f"starting from {startdate}")
            time.sleep(3)
        except:
            startdate = date(2008, 1, 1)
                
        sample = data.get('AAPL',timeframe,premarket)
        index = data.findex(sample,startdate)



        search = sample.iloc[index][0]

        while index < len(sample) - 50:

            search = sample.iloc[index][0]

            Daily.runDaily(search,timeframe)

            index += 1






        #day_count = 1000000000000000
           
        #for single_date in (startdate + timedelta(n) for n in range(day_count)):

            #print(f"////////////////////////////////////// {single_date} //////////////////////////////////////")
            #Daily.runDaily(str(single_date),timeframe)

           # if startdate > date.today():
              #  print("finished")
               #break
        
        
