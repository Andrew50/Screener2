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
from tvDatafeed import TvDatafeed
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
        sFlag = False
        sMover = True
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
                 
                    #print(f"{tick} {indexOfDay} {len(data_daily_full)}")
                    
                    if (dateToSearch == "0"):
                        prevClose = screenbar['Price']
                            
                        pmChange = screenbar['Pre-market Change']
            
                        dolVol = screenbar['Volume*Price']
                        pmPrice = prevClose + pmChange

                        rightedge = indexOfDay 
                        
                    else:
                        pmPrice = data_daily_full.iloc[indexOfDay][1]#open
                        prevClose = data_daily_full.iloc[indexOfDay-1][4] #close
                        dolVol = prevClose*data_daily_full.iloc[indexOfDay-1][5]
                        pmChange = pmPrice/prevClose - 1

                        rightedge = indexOfDay
                         

                    
                    
                    data_daily = data_daily_full[(rightedge - chartSize):(rightedge)]
                    currentday = chartSize
               
                    
                   # data_daily['Datetime'] = pd.to_datetime(data_daily['Date'])
                   # data_daily = data_daily.set_index('Datetime')
                    #data_daily = data_daily.drop(['Date'], axis=1)
                    


                   
                    if(dolVol > 1000000  and prevClose > 3 and pmChange != 0 and math.isnan(pmChange) != True and sEP):
                        Daily.EP(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                    if(dolVol > 5000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sMR):
                        Daily.MR(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                    if(dolVol > 15000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sPivot):
                        Daily.Pivot(data_daily, currentday, pmPrice,screenbar, dateToSearch)
                    if(dolVol > 15000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sMover):
                        Daily.Mover(data_daily, currentday, pmPrice,screenbar, dateToSearch)


    def runDaily(self, dateToSearch):
        if dateToSearch == "0":
            
            tv = TvDatafeed()
            
            data_apple2 = tv.get_hist('AAPL', 'NASDAQ', n_bars=1)
            dateTimeOfDay2 = data_apple2.index[0]
            dateSplit2 = str(dateTimeOfDay2).split(" ")
            date2 = dateSplit2[0]
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            if date2 == today:
               
                if  datetime.datetime.now().hour > 12:
                    print("artificial 0")
                    
                    dateToSearch = date2
                    screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
            else:
                screen.runDailyScan(None)
                screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
                

               
            
                if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                    os.remove("C:/Screener/data_csvs/todays_setups.csv")
        
                god = pd.DataFrame()
                god.to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
            data.runUpdate(tv,False)
        else:
            dateSplit = dateToSearch.split("-")
            x_date = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))

            if(x_date.weekday() >= 5):
                print("The date given is not a weekday.")
                return False
            screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
            data.runUpdate(tv,True)
       
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
            
            # if last three candles are red
            if data_daily.iloc[currentday-1][4] < data_daily.iloc[currentday-1][1] and data_daily.iloc[currentday-2][4] < data_daily.iloc[currentday-2][1] and data_daily.iloc[currentday-3][4] < data_daily.iloc[currentday-3][1]:

                #iterate through last 30 days
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

                #calulate values of today
                todayGapValue = abs((pmPrice/prevClose)-1)
                todayChangeValue = abs(data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1)
                lastCloses = 0
                for c in range(4): 
                    lastCloses = lastCloses + data_daily.iloc[currentday-c-1][4]
                
                fourSMA = (lastCloses/4)
                value = (fourSMA)/pmPrice - 1


                #caclulate zs
                gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
                z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
                
                #requirements
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
        lowergapzfilter = 1
       
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

            if gapz > lowergapzfilter and close1 < ma3 and pmPrice > ma3 and close1 < close2 and close2 < open2 and close1 < open1 :
                
                
                log.daily(screenbar,gapz,"Pivot", dateToSearch,pmPrice) 
           
        except IndexError:
           print(f" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")


    def Mover(data_daily, currentday,pmPrice,screenbar, dateToSearch):
      

        zfilter = 3
        l2 = 10
        l = 100 
        q = deque([])
        z = []
        try: 
            prevClose = data_daily.iloc[currentday-1][4]
            for i in range(l + l2):
                n = l-i - 1
                q.append(data_daily.iloc[currentday-1][4])
                if len(q) >= l2:
                    ma1 = statistics.mean(q)
                    
                    if i >= l2:
                        value = abs(ma2/ma1 - 1)
                        z.append(value)
                    
                    ma2 = ma1
                    q.popleft()
            z = (value - statistics.mean(z))/statistics.stdev(z)
            if z > zfilter:
                
                
                log.daily(screenbar,z,"Mover", dateToSearch,pmPrice) 
           
        except IndexError:
           print(f" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")
            
  





if __name__ == '__main__':
    backtest = False
    day_count = 200
    if backtest:
        #print(datetime.datetime.now())
        start_date = date(2018, 1, 1)
        
        for single_date in (start_date + timedelta(n) for n in range(day_count)):

            Daily.runDaily(Daily, str(single_date))
    else:
        Daily.runDaily(Daily, '0')
