
import pandas as pd
import datetime
import os
import time
from Data5 import Data as data

from Detection1 import Detection as detection

from Scan import Scan as Scan

from UI3 import UI as ui

from pathos.multiprocessing import ProcessingPool as Pool





class Screener:


    def queue(date = '0',tf = None,ticker = None):

        if date == '0':  ##if forecast

            #scan = Scan.get('daily')  
            scan = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
            

            Screener.run('d',scan,date,1,scan)

            ui.loop(ui,True)
            browser = None
            while True:
                browser, scan = Scan.get('intraday',browser)
                Screener.run('1min',scan,date,2,scan)

        else: #if backtest

            
            path = 0
            scan = Scan.get('full')

            if ticker != None: # if a ticker was specified save to todays_setups

                path = 1

                scan = scan[str(ticker)]

            if date != None: # if a date was specified save to todays_setups and run that date

                path = 1

                Screener.run(tf,scan,date,path,None)


            else:

                while True:

                    try:
                        df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                        strdate = df.iloc[len(df)-1][0]
           
                        startdate = datetime.datetime.strptime(strdate, '%Y-%m-%d')
                        print(f"starting from {startdate}")
                        time.sleep(3)
                    except:
                        startdate = date(2008, 1, 1)
                
                    sample = data.get('AAPL',tf)
                    index = data.findex(sample,startdate)

                    while index < len(sample) - 50:

                        date = sample.iloc[index][0]

                        Screener.run(tf,scan,date,path,None)
                       

                        index += 1








    def run(tf,scan,date,path,var):


        if path == 1:
            if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                os.remove("C:/Screener/data_csvs/todays_setups.csv")
            pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)


        screenbars = [] 
        
        for i in range(len(scan)):
            try:
                ticker = str(scan.iloc[i]['Ticker'])
                try:
                    pmPrice = var.loc[str(ticker)]['Pre-market Change'] + var.loc[str(ticker)]['Price']
                except:
                    pmPrice = None
                scan.at[i, 'var'] = pmPrice
                scan.at[i, 'date'] = date
                scan.at[i, 'tf'] = tf
                scan.at[i, 'path'] = path
                screenbars.append(scan.iloc[i])
            except FileNotFoundError:
                print(f"{ticker} delisted")

        with Pool(nodes=7) as pool:
            pool.map(detection.check, screenbars)
        
        



if __name__ == '__main__':

    if True or ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)):
         Screener.queue()









                     






