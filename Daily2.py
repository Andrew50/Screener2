from fileinput import close
import os 
import pandas as pd
import statistics
import math
import datetime
from datetime import date, timedelta
from Log import log as log
import warnings
from pathos.multiprocessing import ProcessingPool as Pool
from tvDatafeed import TvDatafeed,  Interval
warnings.filterwarnings("ignore")
from collections import deque
from Datav4 import Data as data
from Screen import Screen as screen
from UI3 import UI as ui




class Daily:

    


   


    def processTickers(sbr):


        sMR = True
        sEP = True
        sPivot = True
        sFlag = True
  


        chartSize = 80
        rightbuffer = 20
        screenbar = sbr
        tick = str(screenbar['Ticker'])
        dateToSearch = screenbar['dateToSearch']
        print(tick)
        if (os.path.exists("C:/Screener/data_csvs/" + tick + "_data.csv")):
            data_daily_full = pd.read_csv(f"C:/Screener/data_csvs/{tick}_data.csv")
        
            if len(data_daily_full) > 35:
                
                
                
                indexOfDay = data.findIndex(data_daily_full, dateToSearch,False)
                    

                
                if(indexOfDay != 99999):
                 
                    
                    if (dateToSearch == "0"):
                        prevClose = screenbar['Price']
                            
                        pmChange = screenbar['Pre-market Change']
            
                        
                        pmPrice = prevClose + pmChange


                        rightedge = indexOfDay 
                        currentday = chartSize 
                        
                    else:
                        pmPrice = data_daily_full.iloc[indexOfDay][1]
                        prevClose = data_daily_full.iloc[indexOfDay-1][4] 
                        
                        pmChange = pmPrice/prevClose - 1

                        rightedge = indexOfDay
                        currentday = chartSize
                         
                    dolVol = []
                    for i in range(5):
                        dolVol.append(data_daily_full.iloc[indexOfDay-1-i][4]*data_daily_full.iloc[indexOfDay-1-i][5])
                    dolVol = statistics.mean(dolVol)


                    data_daily = data_daily_full[(rightedge - chartSize):(rightedge)]
             
                    
                    if(dolVol > 1000000  and prevClose > 2): 
                        adr = 0
                        try:
                            
                            adrlist = []
                            for j in range(20): 
                                high = data_daily.iloc[currentday-j-1][2]
                                low = data_daily.iloc[currentday-j-1][3]
                                val = (high/low - 1) * 100
                                adrlist.append(val)
                        
                            adr = statistics.mean(adrlist)  
                        except IndexError:
                            print("adr error")
                    
                        if(dolVol > 8000000  and prevClose > 1 and pmChange != 0 and math.isnan(pmChange) != True and adr > 3.5 and sEP):
                            Daily.EP(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                        if(dolVol > 10000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and adr > 5 and sMR):
                            Daily.MR(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                        if(dolVol > 15000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and adr > 3.5 and sPivot):
                            Daily.Pivot(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                        if(dolVol > 10000000  and prevClose > 2 and adr > 4 and sFlag):
                            Daily.Flag(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                    

    def runDaily(self, dateToSearch):
        tv = TvDatafeed()
        if dateToSearch == "0":
            
            
            
            data_apple2 = tv.get_hist('AAPL', 'NASDAQ', n_bars=1, interval=Interval.in_1_minute, extended_session = True)
            dateTimeOfDay2 = data_apple2.index[0]
            dateSplit2 = str(dateTimeOfDay2).split(" ")
            date2 = dateSplit2[0]
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            if date2 == today and (datetime.datetime.now().hour < 12 or (datetime.datetime.now().hour == 12 and datetime.datetime.now().minute <= 15))  :
                #screen.runDailyScan(None)
                screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
                

               
            
                if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                    os.remove("C:/Screener/data_csvs/todays_setups.csv")
        
                god = pd.DataFrame()
                god.to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
          
                
            else:
                print("artificial 0")
                    
                dateToSearch = date2
                screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv") 
            data.runUpdate(tv,False)
        else:
            dateSplit = dateToSearch.split("-")
            x_date = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))

            if(x_date.weekday() >= 5):
                print("The date given is not a weekday.")
                return False
            screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
            #data.runUpdate(tv,True)
       
        screenbars = []
        for i in range(len(screener_data)):
            screener_data.at[i, 'dateToSearch'] = dateToSearch
            screenbars.append(screener_data.iloc[i])
        with Pool(nodes=6) as pool:
            pool.map(Daily.processTickers, screenbars)
        
        if dateToSearch == "0":
            ui.loop(ui,True)


    def EP(data_daily, currentday, pmPrice, screenbar, dateToSearch):
      
        
        zfilter = 7
        
        try: 
            prevClose = data_daily.iloc[currentday-1][4]
            gaps = []
            lows = []
            highs = []
            todayGapValue = ((pmPrice/prevClose)-1)
            for j in range(20): 
                gaps.append((data_daily.iloc[currentday-1-j][1]/data_daily.iloc[currentday-2-j][4])-1)
                lows.append(data_daily.iloc[currentday-j-1][3])
                highs.append(data_daily.iloc[currentday-j-1][2])

            z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
           
            
            if(z > zfilter) and pmPrice > max(highs):
                log.daily(screenbar,z,"EP", dateToSearch,pmPrice) 
            
            elif (z < -zfilter) and pmPrice < min(lows):
                log.daily(screenbar,z,"NEP", dateToSearch,pmPrice) 

        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 
 
    def MR(data_daily, currentday,pmPrice,screenbar, dateToSearch):
        
    
        
        zfilter = 3
        gapzfilter0 = 5.5
        gapzfilter1 = 4
        changezfilter = 2.5
        try: 
            prevClose = data_daily.iloc[currentday-1][4]
            zdata = []
            zgaps = []
            zchange = []
            
        
            if data_daily.iloc[currentday-1][4] < data_daily.iloc[currentday-1][1] and data_daily.iloc[currentday-2][4] < data_daily.iloc[currentday-2][1] and data_daily.iloc[currentday-3][4] < data_daily.iloc[currentday-3][1]:

              
                for i in range(30):
                    n = 29-i
                    gapvalue = abs((data_daily.iloc[currentday-n-1][1]/data_daily.iloc[currentday-n-2][4]) - 1)
                    changevalue = abs((data_daily.iloc[currentday-n-1][4]/data_daily.iloc[currentday-n-1][1]) - 1)
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

             
                todayGapValue = abs((pmPrice/prevClose)-1)
                todayChangeValue = abs(data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1)
                lastCloses = 0
                for c in range(4): 
                    lastCloses = lastCloses + data_daily.iloc[currentday-c-1][4]
                
                fourSMA = (lastCloses/4)
                value = (fourSMA)/pmPrice - 1


            
                gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
                z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
                
              
                if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value > 0):
              
               
                    log.daily(screenbar,z,"MR", dateToSearch,pmPrice) 
               
            
        except IndexError:
           print(" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")
            
    def Pivot(data_daily, currentday,pmPrice,screenbar, dateToSearch):
        

        uppergapzfilter = 8
        lowergapzfilter = 1.8
        lowergapzfilter2 = 1.8
       
        try: 
            prevClose = data_daily.iloc[currentday-1][4]
            zgaps = []
            for i in range(15):
                n = 14-i
                gapvalue = abs((data_daily.iloc[currentday-n-1][1]/data_daily.iloc[currentday-n-2][4]) - 1)
                zgaps.append(gapvalue)
            
            todayGapValue = (pmPrice/prevClose)-1
            gapz = (abs(todayGapValue)-statistics.mean(zgaps))/statistics.stdev(zgaps)
            lastCloses = 0
            for c in range(4): 
                lastCloses = lastCloses + data_daily.iloc[currentday-c-1][4]
                
            ma3 = (lastCloses/4)
            close1 = data_daily.iloc[currentday-1][4]
            close2 = data_daily.iloc[currentday-2][4]
            open1 = data_daily.iloc[currentday-1][1]
            open2 = data_daily.iloc[currentday-2][1]
            low1 = data_daily.iloc[currentday-1][3]
            high1 = data_daily.iloc[currentday-1][2]

            if gapz > lowergapzfilter and close1 < ma3  and close1 < close2 and close2 < open2 and close1 < open1 and open1 < close2 and pmPrice > high1 :
                
                
                log.daily(screenbar,gapz,"Pivot", dateToSearch,pmPrice) 

            if gapz > lowergapzfilter2 and close1 > ma3  and close1 > close2 and close2 > open2 and close1 > open1 and open1 > close2 and pmPrice < low1:

                log.daily(screenbar,gapz,"Pivot", dateToSearch,pmPrice) 
        except IndexError:
           print(f" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")


    def Flag(data_daily, currentday,pmPrice,screenbar, dateToSearch):
        tick = str(screenbar['Ticker'])
        zfilter = 2.2
        lmin = 5
        lmax = 30
        rsil = 20#10 or 15 but for actuall real flag 20 seems best
        zl = 20
        todayl = 0

        try:
            
            rsidata = []
            
            #for i in range(5):
                     #zma = []
                #for j in range(5):
            zdata = []
            for i in range(zl):
                rsilist = []
                rsimax = 0
                for j in range(lmax):
                
                    gains = []
                    losses = []
                    
                    
                    for k in range(rsil):
                        change = (data_daily.iloc[currentday-i-k-j-1][4]/data_daily.iloc[currentday-i-k-j-2][4]) - 1
                        if change > 0:
                            gains.append(change)
                        else:
                            losses.append(-change)


                    RS = (sum(gains)/rsil) / (sum(losses)/rsil)
                    rsi = abs((100 - (100 / (1 + RS))) - 50)
                    rsilist.append(rsi)
                    if rsi > rsimax:
                        rsimax = rsi
                        l = j
                
                #print(str(f"{tick} , {l}"))
                
                gaindata = []
                flagdata = []
                if l < 2:
                    l = 2
                if i == 0:
                    todayl = l
                for j in range((l-1) * 2):
                    ma3 = []
                    for k in range(2):

                        ma3.append(data_daily.iloc[currentday-i-j-k-1][4])
                    ma3 = statistics.mean(ma3)
                            
                    if j >= l - 1:
                        gaindata.append(ma3)
                    else:

                        flagdata.append(ma3)
                    
                gain = max(gaindata)/min(gaindata)
                flag = max(flagdata)/min(flagdata)
               
                value = gain - flag
                if i > 0:

                    zdata.append(value)
                else:
                    currentvalue = value
              
            z = (currentvalue - statistics.mean(zdata))/statistics.stdev(zdata)
            
            if z > zfilter and todayl > lmin:
                log.daily(screenbar,z,"Flag", dateToSearch,pmPrice) 
        except ValueError:
            print("value error")
        except IndexError:
           print(f" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")
        except statistics.StatisticsError:
            print("stats error")
if __name__ == '__main__':
    backtest = False
    day_count = 100
    if backtest:
        start_date = date(2022, 1, 1)
        
        for single_date in (start_date + timedelta(n) for n in range(day_count)):

            Daily.runDaily(Daily, str(single_date))
    else:
        Daily.runDaily(Daily, '0')
                  