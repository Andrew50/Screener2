

from re import T
import pandas as pd
import datetime
import os
import time
from tqdm import tqdm
from Data7 import Data as data

from Detection2 import Detection as detection

from Scan import Scan as scan

from UI3 import UI as ui

from Consolidator import consolidate



#from pathos.multiprocessing import ProcessingPool as Pool






class Screener:


    def queue(date = None,days = 1, ticker = None, tf = 'd',browser = None, fpath = None):
        
        path = 0
        date_buffer = 20

        consolidate.consolidate()

        
        df ={'Date': [],
                    'Ticker':[],
                    'Setup': [],
                    'Z': [],
                    'tf':[]}
        pd.DataFrame(df).to_feather("C:/Screener/tmp/todays_setups.feather")
        if ticker == None:
            
            ticker_list = scan.get(date,tf,True,browser).index.tolist()
            
           
            if date == None:
                i = 0
                try:
                    df = pd.read_feather(r"C:\Screener\tmp\setups.feather")

                    
                    god = df['Ticker'].tolist()
                    
                    for ticker in god:
                        try:
                            ticker_list.remove(ticker)
                            i += 1
                        except:
                            pass
                    
                except FileNotFoundError:
                    pass
                print(f'{i} tickers already completed')

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
            sample = data.get('AAPL',tf)
            if date == None:
                '''
                startdate = datetime.date(2008, 1, 1)
                enddate = datetime.datetime.now()# - datetime.timedelta(date_buffer)

                start_index = data.findex(sample,startdate)
                end_index = data.findex(sample,enddate)
                trim = sample[start_index:end_index]
                
                date_list = trim.index.tolist()
                '''
                date_list =sample.index.tolist()
                

            else:
                path = 1
                #startdate = datetime.datetime.strptime(date, '%Y-%m-%d')
                
                start_index = data.findex(sample,date)  
                end_index = start_index + days

                trim = sample[start_index:end_index]
                
                date_list = trim.index.tolist()
              
            
        if fpath != None:
            path = fpath

        
        Screener.run(date_list, ticker_list, tf,path)

    
    def run(date_list,ticker_list,tf,path):
        length = len(ticker_list)*len(date_list)
        pbar = tqdm(total=length)
        container = []
       
        for i in  range(len( ticker_list)):
            
            ticker = ticker_list[i]
            
            container.append([ticker, tf , path, []])

            for date in date_list:
                    
                container[i][3].append(date)
                pbar.update(1)
                    
        
        pbar.close()
        data.pool(detection.check, container)
        

if __name__ == '__main__':
   
    if   ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)):

        Screener.queue('0')
         
        ui.loop(ui,True)
         
        browser = scan.startFirefoxSession()
        while datetime.datetime.now().hour < 13:
           
            Screener.queue(tf = '1min', date = '0',browser = browser)

    else:
        
        #Screener.queue(date = '2022-01-01',fpath = 0,days = 5)
        Screener.queue()
        #ui.loop(ui,False)
       
       
       










                     



