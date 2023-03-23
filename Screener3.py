

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


    def queue(date = None,ticker = None, tf = 'd'):
        if date == '0':
            date = datetime.datetime.today()
        date_buffer = 20

        if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
            os.remove("C:/Screener/data_csvs/todays_setups.csv")
        pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)

        
        if date == None:
            try:
                df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                try:
                    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                except:
                    
                    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except:
                startdate = datetime.date(2022, 1, 1)

            sample = data.get('AAPL',tf)
            index = data.findex(sample,startdate)

            trim = sample[index + 1:-date_buffer]
            
            date_list = trim['datetime'].tolist()

            
        elif type(date) is str or type(date) == datetime.datetime:
            date_list = [date]
           
	
        else:
            date_list = date
            



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
        print(ticker_list)
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

    if True or ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)):

         Screener.queue('0')

    else:
        
        Screener.queue(ticker = ['COIN','HOOD'])









                     


