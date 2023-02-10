import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import statistics
from Screen import Screen as screen
import datetime
from discordManager import discordManager as dM
from functools import partial
from itertools import repeat
from pathos.multiprocessing import ProcessingPool as Pool
class Intraday:
    def runTicker(screenb):
        screenbar = screenb
        exchange = str(screenbar['Exchange'])
        dayChange = round(screenbar['Change %'], 2)
        currPrice = screenbar['Price']
        dolVol = screenbar['Volume*Price']
        tick = str(screenbar['Ticker'])
        print(tick)
        oneMinChange = screenbar['Change 1m, %']
        return 'test' + f" {tick}"
        try:
            if (dolVol > 7500000 and currPrice > 1.2):
                if(oneMinChange > 1 or dayChange > 11):
                    tvr = TvDatafeed()
                    data_minute = tvr.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=1000)

                    if( dolVol > 7500000 and currPrice > 1.2 ):#and (counter % 5 == 0)): 
                        Intraday.Gainers(data_minute, screenbar,dayChange)

                    if(dolVol > 750000 and currPrice > 1.2):
                        Intraday.Pops(data_minute, screenbar)
        except TypeError:
            print(f' {tick} did not return data!')
        except AttributeError:
            print(' {tick} did not return data!')
    def runIntraday(tvlog, brows):
        br = brows
        tvr = tvlog
        #if(tvr == None):
        #    tvr = screen.logInScrapper()
        #br = screen.runIntradayScan(br)
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        numTickers = len(screener_data)
        print(datetime.datetime.now())
        screenBars = []
        for i in range(numTickers):
            screenBars.append(screener_data.iloc[i])
           
        pool = Pool(nodes=8)
        print(pool.map(Intraday.runTicker, screenBars))
        print(datetime.datetime.now())
        return tvr, br
            

    def Gainers(data_minute, screenbar,dayChange):
        if(dayChange > 15):
            z = 0
            dM.post(data_minute,screenbar,z,"Gainer","0")

    def Pops(data_minute, screenbar):

        zfilter = 50

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
                dM.post(data_minute,screenbar,z,"Pop","0")
        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 
  
                
                


if __name__ == '__main__':
    Intraday.runIntraday(None, None)
