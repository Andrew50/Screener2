import os 
import time 
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
import statistics
import mplfinance as mpf
import matplotlib as mpl
import pathlib
import math

from discordManager import discordManager as dM

import warnings
warnings.filterwarnings("ignore")
class Daily:

    #def __init__(self):
    
    def sfindIndex(df, dateTo):
        for i in range(len(df)):
            dateTimeOfDay = df.iloc[i]['datetime']
            dateSplit = str(dateTimeOfDay).split(" ")
            date = dateSplit[0]
        
            if(date == dateTo):
                return i

        return 99999

    def runDaily(self, dateToSearch):
        
      
        chartSize = 80
        rightbuffer = 20
        sMR = True
        sEP = False
        sPivot = False
        sFlag = False
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        numTickers = len(screener_data)

        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)

            #Loop stocks in screen
        
        for i in range(numTickers):
            tick = str(screener_data.iloc[i]['Ticker'])
            exchange = str(screener_data.iloc[i]['Exchange'])
            pmChange = screener_data.iloc[i]['Pre-market Change']
            currPrice = screener_data.iloc[i]['Price']
            volume = screener_data.iloc[i]['Volume']
            dolVol = screener_data.iloc[i]['Volume*Price']
            # Gaps Check 
            #print(tick + f" {i}")
            if (os.path.exists("C:/Screener/data_csvs/" + tick + "_data.csv")):
                data_daily_full = pd.read_csv(f"C:/Screener/data_csvs/{tick}_data.csv")
        
                if len(data_daily_full) > 50:
                
                    indexOfDay = self.sfindIndex(data_daily_full, dateToSearch)
                    if(indexOfDay != 99999):
                    
                        if (dateToSearch == "0"):
                            pmPrice = prevClose + pmChange
                            rightedge = len(data_daily_full)
                        else:
                            pmPrice = data_daily_full.iloc[indexOfDay][2]
                            if len(data_daily_full) - indexOfDay > rightbuffer:
                                rightedge = indexOfDay+rightbuffer
                                currentday = chartSize-rightbuffer
                            else:
                                rightedge = len(data_daily_full)
                                currentday = chartSize-(len(data_daily_full) - rightedge)



                        data_daily = data_daily_full[(rightedge - chartSize):(rightedge)]
                        data_daily['Datetime'] = pd.to_datetime(data_daily['datetime'])
                        data_daily = data_daily.set_index('Datetime')
                        data_daily = data_daily.drop(['datetime'], axis=1)
                        #print(rightedge)
                        #print(len(data_daily_full))
                    
                        self.EP(tick, dolVol, volume, currPrice, data_daily,currentday,pmPrice, pmChange, dateToSearch, sEP, s)
                        self.MR(tick, dolVol, volume, currPrice, data_daily,currentday,pmPrice, pmChange, dateToSearch, sMR, s)

    def EP(tick, dolVol, volume, currPrice, data_daily,currentday,pmPrice, pmChange, dateToSearch, EP, s):
        if(dolVol > 1000000 and volume>150000 and currPrice > 3 and EP):
            try: 
                gaps = []
             
                prevClose = data_daily.iloc[currentday-1][5]
                todayGapValue = round(((pmPrice/prevClose)-1), 2)
                for j in range(20): 
                        gaps.append((data_daily.iloc[currentday-1-j][2]/data_daily.iloc[currentday-2-j][5])-1)

                z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)

                if(z < -5):
                    z = round(z, 3)
                    ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
                    todayGapValuePercent = todayGapValue*100;
                    mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                    dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▼ {pmChange} ({todayGapValuePercent}%)", f"NEP Setup, Z-Score: {z}")
                    dM.sendDiscordPost('tmp/test.png')
                if(z > 5):
                    z = round(z, 3)
                    ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
                    todayGapValuePercent = todayGapValue*100;
                    mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                    dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"EP Setup, Z-Score: {z}")
                    dM.sendDiscordPost('tmp/test.png')
                print(tick)
            except IndexError:
                print(tick + " doesnt exist " + dateToSearch)
            except TimeoutError:
                    print("Timeout caught")
            except FileNotFoundError:
                print(tick + " does not have a file") 
            #except TypeError:
                #print(tick + " line 84 bs") 
     

                                #MR###############################################################################
    def MR(tick, dolVol, volume, currPrice, data_daily,currentday,pmPrice, pmChange, dateToSearch, MR, s):
        if(dolVol > 1000000 * 1000 and volume > 150000 and currPrice > 2 and pmChange != 0 and math.isnan(pmChange) != True and MR):
            try: 
                
                zfilter = 3.2
                gapzfilter0 = 8
                gapzfilter1 = 4
                changezfilter = 4
			
                prevClose = data_daily.iloc[currentday-1][5]
                    
                todayGapValue = round(((pmPrice/prevClose)-1), 2)
                todayChangeValue = data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1
                zdata = [] # 15 currentday
                zgaps = [] # 30 currentday=
                zchange = [] # 30 currentday
                for i in range(30):
                    n = 29-i
                    gapvalue = abs((data_daily.iloc[currentday-n-1][2]/data_daily.iloc[currentday-2-n][5]) - 1)
                    changevalue = abs((data_daily.iloc[currentday-1-n][5]/data_daily.iloc[currentday-1-n][2]) - 1)
                    lastCloses = 0
                    for c in range(4): 
                    
                        lastCloses = lastCloses + data_daily.iloc[currentday-2-c-n][5]
                    fourSMA = round((lastCloses/4), 2)
                    datavalue = (fourSMA/data_daily.iloc[currentday-n-1][2] - 1)
                    if i == 29:
                        gapz1 = (gapvalue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                    zgaps.append(gapvalue)
                    zchange.append(changevalue)
                    if i > 14:
                        zdata.append(datavalue)
				
				
				
                gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
                lastCloses = 0
                for c in range(4): 
                    
                    lastCloses = lastCloses + data_daily.iloc[currentday-c-n][5]
                fourSMA = round((lastCloses/4), 2)
                value3 = (fourSMA)/pmPrice
                z = (value3 - statistics.mean(zdata))/statistics.stdev(zdata) 
			
			
                
                if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value3 > 0):
                    z = round(z, 3)
                    ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
                    todayGapValuePercent = todayGapValue*100;
                    mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                    dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
                    dM.sendDiscordPost('tmp/test.png')
                print(tick)
            except IndexError:
                print(tick + " did not exist at the date " + dateToSearch)
            except TimeoutError:
                print("Timeout caught")
            except FileNotFoundError:
                print(tick + " does not have a file")   
        return 'done'
    

    


    
    

    


#Daily.runDaily(Daily,'2022-05-12')
            #if(dolVol > 1000000 and volume > 150000 and currPrice > 2 and pmChange != 0 and math.isnan(pmChange) != True and Pivot):

            #if(dolVol > 1000000 and volume > 150000 and currPrice > 2 and pmChange != 0 and math.isnan(pmChange) != True and Flag):

    