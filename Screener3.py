

from re import T
import pandas as pd
import datetime
import os
import time
from tqdm import tqdm
from Data6 import Data as data

from Detection1 import Detection as detection

from Scan import Scan as scan

from UI3 import UI as ui

#from pathos.multiprocessing import ProcessingPool as Pool






class Screener:


    def queue(date = None,days = 1, ticker = None, tf = 'd',browser = None):
        
        path = 0
        date_buffer = 20

        if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
            os.remove("C:/Screener/data_csvs/todays_setups.csv")
        pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
        if ticker == None:
            ticker_list = scan.get(date,tf,browser)['Ticker'].tolist()

        elif type(ticker) is str:
            path = 1
            ticker_list = [ticker]
	       
        else:
            path = 1
            ticker_list = ticker
        if date == '0':
            if tf == 'd' or tf == 'w' or tf == 'm':
                path = 1
            else:
                path = 2
            date_list = [date]
        else:
            if date == None:
                if path == 0:
                    try:
                        df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                        dt = df.iloc[-1][0]
                        startdate = datetime.datetime.strptime(dt, '%Y-%m-%d')
                    except:
                        startdate = datetime.date(2008, 1, 1)
                else:
                    startdate = datetime.date(2008, 1, 1)
                enddate = datetime.datetime.now() - datetime.timedelta(date_buffer)

            else:
                path = 1
                startdate = datetime.datetime.strptime(date, '%Y-%m-%d')
               
                enddate = startdate + datetime.timedelta(days)



            sample = data.get('AAPL',tf)
            
            start_index = data.findex(sample,startdate)  
            end_index = data.findex(sample, enddate) 

           

            trim = sample[start_index:end_index]
            
            date_list = trim['datetime'].tolist()

  

        
            

        

        Screener.run(date_list, ticker_list, tf,path)

        
  



    def run(date_list,ticker_list,tf,path):


        container = []
        for date in date_list:
            
            for ticker in ticker_list:
                    
                    container.append([date,ticker,tf,path])

                    #if len(container) > poolsize:
                        #Screener.pool(container)

                        #container = []

       
        data.pool(detection.check, container)
        
    


if __name__ == '__main__':
    test = True
    if test or  ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)):

        Screener.queue('0')
         
        ui.loop(ui,True)
         
        browser = scan.startFirefoxSession()
      #  while True:
           
       #     Screener.queue(tf = '1min', date = '0',browser = browser)

    else:
        #Screener.queue('0')
        #Screener.queue(date = '2023-03-21')
        Screener.queue(ticker = ['NVAX'])
        #.queue()
        #Screener.queue(tf = '1min', date = '0')
        #Screener.queue(date = '2023-03-16', tf = '2h',ticker = ['HOOD'], days = 1)
        ui.loop(ui,True)










                     


