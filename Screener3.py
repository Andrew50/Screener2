

from re import T
import pandas as pd
import datetime
import os
import time
from Data5 import Data as data

from Detection1 import Detection as detection

from Scan import Scan as scan

from UI3 import UI as ui

from pathos.multiprocessing import ProcessingPool as Pool





class Screener:


    def queue(date = None,days = 1, ticker = None, tf = 'd'):
        
        date_buffer = 20

        if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
            os.remove("C:/Screener/data_csvs/todays_setups.csv")
        pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)

        if date == '0':
            date_list = [date]
        else:
            if date == None:
                try:
                    df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                    dt = df.iloc[-1][0]
                    startdate = datetime.datetime.strptime(dt, '%Y-%m-%d')
                except:
                    startdate = datetime.date(2022, 1, 1)

                enddate = datetime.datetime.now() - datetime.timedelta(date_buffer)

            else:
                startdate = datetime.datetime.strptime(date, '%Y-%m-%d')
               
                enddate = startdate + datetime.timedelta(days)



            sample = data.get('AAPL',tf)
            
            start_index = data.findex(sample,startdate)  
            end_index = data.findex(sample, enddate) 

            #print(f'{start_index} , {end_index}')
            #print(f'{sample.iloc[start_index][0]} , {sample.iloc[end_index][0]}')

            trim = sample[start_index:end_index]
            
            date_list = trim['datetime'].tolist()

  

        if ticker == None:
            ticker_list = scan.get(date,tf)['Ticker'].tolist()

        elif type(ticker) is str:
            ticker_list = [ticker]
	       
        else:
            ticker_list = ticker
            

        

        Screener.run(date_list, ticker_list, tf)

        
    def pool(container):
        with Pool(nodes=7) as pool:
            pool.map(detection.check, container)


    def run(date_list,ticker_list,tf):

        
        
        poolsize = 5000
        container = []
        for date in date_list:
           
            for ticker in ticker_list:
                    
                    container.append([date,ticker,tf])

                    if len(container) > poolsize:
                        Screener.pool(container)

                        container = []


        Screener.pool(container)



if __name__ == '__main__':

    if ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)):

         Screener.queue('0')
         ui.loop(ui,True)
         while True:
           Screener.queue(tf = '1min', date = '0')

    else:
        #Screener.queue('0')
        #Screener.queue(date = '2023-03-21')
        #Screener.queue(ticker = ['COIN','HOOD'])
        #Screener.queue(ticker = ['COIN','HOOD'],tf = '1min', date = '0')
        Screener.queue(tf = '1min', date = '0')
        #Screener.queue(date = '2023-03-16', tf = '2h',ticker = ['HOOD'], days = 1)
        ui.loop(ui,True)










                     


