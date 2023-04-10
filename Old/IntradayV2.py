import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import statistics
from Screen import Screen as screen
import datetime
from Log import log as log
from functools import partial
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool

class Intraday:
    def findIndex(df, dateTo):

        pass


    def runTickerList(screenb):
        screenbar = screenb
        exchange = str(screenbar['Exchange'])
        dayChange = round(screenbar['Change %'], 2)
        currPrice = screenbar['Price']
        dolVol = screenbar['Volume*Price']
        tick = str(screenbar['Ticker'])
        print(tick)
        oneMinChange = screenbar['Change 1m, %']
        try:
            if (dolVol > 7500000 and currPrice > 1.2):
                if(oneMinChange > 1 or dayChange > 11):
                    if( dolVol > 7500000 and currPrice > 1.2 ):#and (counter % 5 == 0)): 
                        return screenbar, "Gainers"

                    if(dolVol > 750000 and currPrice > 1.2):
                        return screenbar, "Pops"
        except TypeError:
            print(f' {tick} did not return data!')
        except AttributeError:
            print(' {tick} did not return data!')
    def processTickers(tickerList):
        gainers = []
        pops = []
        for i in range(len(tickerList)):
            if(tickerList[i][1] == "Gainers"):
                gainers.append(tickerList[i][0])
            if(tickerList[i][1] == "Pops"):
                pops.append(tickerList[i][0])
        with Pool(nodes=6) as pool:
            pool.map(Intraday.Gainers, gainers)
        with Pool(nodes=6) as pool:
            test = pool.map(Intraday.Pops, pops)
        
        

    def runIntraday(tvlog, brows):
        br = brows
        tvr = tvlog
        if(tvr == None):
            tvr = screen.logInScrapper()
        br = screen.runIntradayScan(br)
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        numTickers = len(screener_data)
        screenBars = []
        for i in range(numTickers):
            screenBars.append(screener_data.iloc[i])
        returnedScreenbars = []
        with Pool(nodes=8) as pool:
            returnedScreenbars = pool.map(Intraday.runTickerList, screenBars)
        setupScreenbars = []
        for i in range(len(returnedScreenbars)):
            if(returnedScreenbars[i] != None):
                setupScreenbars.append(returnedScreenbars[i])
        print(setupScreenbars)
        Intraday.processTickers(setupScreenbars)
        return tvr, br
            
    def fiveMinFade():
        print("n")
    def Gainers(screenbar):
        try:
            dayChange = round(screenbar['Change %'], 2)
            if(dayChange > 15):
                tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
            
                exchange = str(screenbar['Exchange'])
                tick = str(screenbar['Ticker'])
                data_minute = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=1000)
                z = 0
                log.intraday(data_minute,screenbar,z,"Gainer")
                print(tick + " sent ")
        except PermissionError:
            print('Permission Error Caught')

    def Pops(screenbar):

        zfilter = 50
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        exchange = str(screenbar['Exchange'])
        tick = str(screenbar['Ticker'])
        print(tick)
        data_minute = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=1000)
        print(data_minute)
        try:
            data = []
            length = len(data_minute)
            for i in range(len(data_minute)): 
                x = data_minute.iloc[i][5] + data_minute.iloc[i-1][5]
                y = ((data_minute.iloc[i][4]/data_minute.iloc[i][1]) + (data_minute.iloc[i][4]/data_minute.iloc[i][1]) - 2)
                value = x*pow(y,2)
                if i != length - 1:
                    data.append(value)
             
            z = (value-statistics.mean(data))/statistics.stdev(data)
            if ((z < -zfilter) or (z > zfilter)) and y > 2:
                log.intraday(data_minute,screenbar,z,"Pop")
                #return data_minute, screenbar, z, "Pop", "0"
        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 
  
                
                


if __name__ == '__main__':
   Intraday.runIntraday(None, None)
