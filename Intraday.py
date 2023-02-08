﻿import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import statistics
from Screen import Screen as screen
from discordManager import discordManager as dM
class Intraday:
    def runIntraday(tvlog, brows):
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        br = brows
        tvr = tvlog
        if(tvr == None):
            tvr = screen.logInScrapper()
        br = screen.runIntradayScan(br)
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        numTickers = len(screener_data)
        for i in range(numTickers):
            screenbar = screener_data.iloc[i]
            exchange = str(screenbar['Exchange'])
            dayChange = round(screenbar['Change %'], 2)
            currPrice = screenbar['Price']
            dolVol = screenbar['Volume*Price']
            tick = str(screenbar['Ticker'])
            
            print(tick)

            if (dolVol > 7500000 and currPrice > 1.2):
                data_minute = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=1000)

                if( dolVol > 7500000 and currPrice > 1.2 ):#and (counter % 5 == 0)): 
                    Intraday.Gainers(data_minute, screenbar,dayChange)

                if(dolVol > 750000 and currPrice > 1.2):
                    Intraday.Pops(data_minute, screenbar)
            
        return tvr, br
            

    def Gainers(data_minute, screenbar,dayChange):
        if(dayChange > 15):
            z = 0
            try:
                dM.post(data_minute,screenbar,z,"Gainer","0")
            except TypeError:
                print(' did not return data!')

    def Pops(data_minute, screenbar):

        zfilter = 50

        try:
            data = []
            length = len(length)
            for i in range(len(data_minute)): 
                x = data_minute.iloc[i][5] + data_minute.iloc[i-1][5]
                y = ((data_minute.iloc[i][4]/data_minute.iloc[i][1]) + (data_minute.iloc[i][4]/data_minute.iloc[i][1]) - 2)
                value = x*pow(y,2)
                if i != length - 1:
                    data.append(value)
             
            z = (value-statistics.mean(data))/statistics.stdev(data)
            if ((z < -zfilter) or (z > zfilter)) and y > 2:
                dM.post(data_minute,screenbar,z,"Pop","0")
        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 

        
                
                


