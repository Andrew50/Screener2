﻿import os 
import pandas as pd
import statistics
import math

from discordManager import discordManager as dM

import warnings
warnings.filterwarnings("ignore")
class Daily:

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
        for i in range(numTickers):
            screenbar = screener_data.iloc[i]
            tick = str(screenbar['Ticker'])
            pmChange = screener_data.iloc[i]['Pre-market Change']
            prevClose = screener_data.iloc[i]['Price']
            dolVol = screener_data.iloc[i]['Volume*Price']
            print(tick)
            if (os.path.exists("C:/Screener/data_csvs/" + tick + "_data.csv")):
                data_daily_full = pd.read_csv(f"C:/Screener/data_csvs/{tick}_data.csv")
        
                if len(data_daily_full) > 50:
                
                    indexOfDay = self.sfindIndex(data_daily_full, dateToSearch)
                    if(indexOfDay != 99999):
                    
                        if (dateToSearch == "0"):
                            pmPrice = prevClose + pmChange
                            rightedge = len(data_daily_full)
                        else:
                            pmPrice = data_daily_full.iloc[indexOfDay][2]#close
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
                        
                        if(dolVol > 1000000  and prevClose > 3 and sEP):
                            self.EP(data_daily, currentday, pmPrice, prevClose,screenbar)
                        if(dolVol > 5000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sMR):
                            self.MR(data_daily, currentday, pmPrice, prevClose,screenbar)

    def EP(data_daily, currentday, pmPrice, prevClose, screenbar ):

        zfilter = 5

        try: 
            gaps = []
            todayGapValue = round(((pmPrice/prevClose)-1), 2)
            for j in range(20): 
                    gaps.append((data_daily.iloc[currentday-1-j][1]/data_daily.iloc[currentday-2-j][4])-1)
            z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
            if(z < -zfilter) or (z > zfilter):
                dM.post(data_daily,screenbar,z,"EP",currentday) 
        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 
 
    def MR(data_daily, currentday,pmPrice,prevClose,screenbar):

        zfilter = 3.2
        gapzfilter0 = 8
        gapzfilter1 = 4
        changezfilter = 4

        try: 
            zdata = []
            zgaps = []
            zchange = []
            for i in range(30):
                n = 29-i
                gapvalue = abs((data_daily.iloc[currentday-n-1][1]/data_daily.iloc[currentday-2-n][4]) - 1)
                changevalue = abs((data_daily.iloc[currentday-1-n][4]/data_daily.iloc[currentday-1-n][1]) - 1)
                lastCloses = 0
                    
                for c in range(4): 
                    
                    lastCloses += data_daily.iloc[currentday-2-c-n][4]
                fourSMA = (lastCloses/4)
                datavalue = abs(fourSMA/data_daily.iloc[currentday-n-1][1] - 1)
                if i == 29:
                    gapz1 = (gapvalue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                zgaps.append(gapvalue)
                zchange.append(changevalue)
                if i > 14:
                    zdata.append(datavalue)
            todayGapValue = round(((pmPrice/prevClose)-1), 2)
            todayChangeValue = data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1
            gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
            changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
            lastCloses = 0

            for c in range(4): 
                lastCloses = lastCloses + data_daily.iloc[currentday-c-n][4]
            fourSMA = round((lastCloses/4), 2)
            value = (fourSMA)/pmPrice - 1

            z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
            if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value3 > 0):
                dM.post(data_daily,screenbar,z,"MR",currentday)     
            
        except IndexError:
            print(tick + " did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(tick + " does not have a file")   
        
    