

import os
import pandas as pd
import statistics
import time
import datetime
from datetime import date, timedelta
from Log2 import log as log
import warnings
from pathos.multiprocessing import ProcessingPool as Pool
from tvDatafeed import TvDatafeed
warnings.filterwarnings("ignore")
from Data5 import Data as data
from Scan import Scan as screen
from UI3 import UI as ui




class Daily:

    

    def processTickers(screenbar):

        try:
            
            timeframe = str(screenbar['interval'])
            ticker = str(screenbar['Ticker'])
            dateToSearch = screenbar['dateToSearch']
            print(ticker)
            dolVol, adr = Daily.requirements(ticker,dateToSearch)

            

            if dolVol > 10000000 and adr > 3.5:

                
                df = data.get(ticker,timeframe)
                currentday = data.findex(df,dateToSearch)
        
                

                if (dateToSearch == "0"):    
                   
                    pmPrice = df.iloc[currentday-1][4] + screenbar['Pre-market Change']
       
                else:
                    
                    pmPrice = df.iloc[currentday][1]

                sEP = True
                sMR = True
                sPivot = True
                sFlag = True
                dolVolFilter = 10000000

                if(dolVol > .2* dolVolFilter  and adr > 3.5 and sEP):
                    Daily.EP(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > .8 * dolVolFilter    and adr > 5 and sMR):
                    Daily.MR(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > 1* dolVolFilter   and adr > 3.5 and sPivot):
                    Daily.Pivot(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
                if(dolVol > .8 * dolVolFilter   and adr > 4 and sFlag):
                    Daily.Flag(df, currentday, pmPrice,screenbar, dateToSearch,timeframe)
        except FileNotFoundError: 
            print(f"{ticker} is delisted")
        except:
            print(f"{ticker} failed")

            
            
    def get_list(dateToSearch,ticker):

        
        if ticker != None:
            full = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")
            screener_data  = full.iloc[str(ticker)]
        else:
            tv = TvDatafeed()
            if dateToSearch == "0":
            
                screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
                if(os.path.exists("C:/Screener/data_csvs/todays_setups.csv")):
                    os.remove("C:/Screener/data_csvs/todays_setups.csv")
                pd.DataFrame().to_csv(("C:/Screener/tmp/todays_setups.csv"),  header=False)
                #
                #screen.runDailyScan(None)
                #data.runUpdate()

            else:
                
                if(dateToSearch.weekday() >= 5):
                    print("The date given is not a weekday.")
                    return False
                screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")

            return screener_data

    def runDaily(dateToSearch = '0', interval = 'd',ticker = None):
        
        screener_data = Daily.get_list(dateToSearch,ticker)

        screenbars = []
        for i in range(len(screener_data)):
            screener_data.at[i, 'dateToSearch'] = dateToSearch
            screener_data.at[i, 'interval'] = interval
            screenbars.append(screener_data.iloc[i])

        with Pool(nodes=6) as pool:
            pool.map(Daily.processTickers, screenbars)
        
        if dateToSearch == "0":
            ui.loop(ui,True)

    def requirements(ticker,date):
        try:
            df = data.get(ticker,'d')
            currentday = data.findex(df,date)
            if(currentday == None): 
                print('god')
                return 0, 0 
            dolVol = []
            for i in range(5):
                dolVol.append(df.iloc[currentday-1-i][4]*df.iloc[currentday-1-i][5])
            dolVol = statistics.mean(dolVol)

       
                            
            adr= []
            for j in range(20): 
                high = df.iloc[currentday-j-1][2]
                low = df.iloc[currentday-j-1][3]
                val = (high/low - 1) * 100
                adr.append(val)
                        
            adr = statistics.mean(adr)  
       
            return dolVol, adr
        except:
            print('req failed')
            return 0 , 0

    def EP(data_daily, currentday, pmPrice, screenbar, dateToSearch,timeframe):
      
        
        zfilter = 5.5
        
      #  try: 
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
            log.daily(screenbar,z,"EP", dateToSearch,pmPrice,data_daily,currentday,timeframe) 
            
        elif (z < -zfilter) and pmPrice < min(lows):
            log.daily(screenbar,z,"NEP", dateToSearch,pmPrice,data_daily,currentday,timeframe) 

      #  except IndexError:
       #     print("index error")
     #   except TimeoutError:
         #   print("timeout error")
      #  except FileNotFoundError:
         #   print("file error") 

    
 
    def MR(data_daily, currentday,pmPrice,screenbar, dateToSearch,timeframe):
        
    
        
        zfilter = 3.5
        gapzfilter0 = 5.5
        gapzfilter1 = 4
        changezfilter = 2.5
       # try: 
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
              
               
                log.daily(screenbar,z,"MR", dateToSearch,pmPrice,data_daily,currentday,timeframe) 
               
      
    def Pivot(data_daily, currentday,pmPrice,screenbar, dateToSearch,timeframe):
        

       
        lowergapzfilter = 1.5
        lowergapzfilter2 = 1.5
       
       # try: 
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
                
                
            log.daily(screenbar,gapz,"Pivot", dateToSearch,pmPrice,data_daily,currentday,timeframe) 

        if gapz > lowergapzfilter2 and close1 > ma3  and close1 > close2 and close2 > open2 and close1 > open1 and open1 > close2 and pmPrice < low1:

            log.daily(screenbar,gapz,"Pivot", dateToSearch,pmPrice,data_daily,currentday,timeframe) 
      


    def Flag(data_daily, currentday,pmPrice,screenbar, dateToSearch,timeframe):
        tick = str(screenbar['Ticker'])
        
        
        if dateToSearch == "0":
            zfilter = 4
        else:
            zfilter = 8


        z2filter = .25
        lmin = 5
        lmax = 20
        rsil = 20
        zl = 20
        rsi_filter = 25
        todayl = 0
        currentvalue = 0

       
            
        rsimax = 0
        for j in range(lmax):
                
            gains = []
            losses = []
                    
                    
            for k in range(rsil):
                change = (data_daily.iloc[currentday-k-j-1][4]/data_daily.iloc[currentday-k-j-2][4]) - 1
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(-change)


            RS = (sum(gains)/rsil) / (sum(losses)/rsil)
            rsi = abs((100 - (100 / (1 + RS))) - 50)
               
            if rsi > rsimax:
                rsimax = rsi
                l = j - 1
                
          
                
        gaindata = []
        flagdata = []
            
        halfdata = []
                
        if l > lmin and l < lmax - 2 and rsimax > rsi_filter:
            for j in range(l * 2):
                ma3 = []
                for k in range(3):

                    ma3.append(data_daily.iloc[currentday-j-k-1][4])
                ma3 = statistics.mean(ma3)
                          
                if j < int(l/2):
                    halfdata.append(ma3)

                if j >=l:
                    gaindata.append(ma3)
                else:

                    flagdata.append(ma3)
                    
            gain = max(gaindata) - min(gaindata)
            flag = max(flagdata) - min(flagdata)
               
            halfflag = max(halfdata) - min(halfdata) 

            value = gain - flag
                

            zdata = []
            
            for i in range(zl):
                pushvalue = data_daily.iloc[currentday-i-1][2] - data_daily.iloc[currentday-i-1][3]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            if z > zfilter and z2 > z2filter:
                    
                log.daily(screenbar,z,"Flag", dateToSearch,pmPrice,data_daily,currentday,timeframe) 

      

    def weeklyFlag(data_daily, currentday,pmPrice,screenbar, dateToSearch,timeframe):
        tick = str(screenbar['Ticker'])
        zfilter = 5
        z2filter = -100
        lmin = 20
        lmax = 50
        rsil = 20
        zl = 20
        rsi_filter = 30
        

        
            
            
        rsimax = 0
        for j in range(lmax):
                
            gains = []
            losses = []
                    
                    
            for k in range(rsil):
                change = (data_daily.iloc[currentday-k-j-1][4]/data_daily.iloc[currentday-k-j-2][4]) - 1
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(-change)


            RS = (sum(gains)/rsil) / (sum(losses)/rsil)
            rsi = abs((100 - (100 / (1 + RS))) - 50)
               
            if rsi > rsimax:
                rsimax = rsi
                l = j - 1
                
          
                
        gaindata = []
        flagdata = []
            
        halfdata = []
                
        if l > lmin and l < lmax - 2 and rsimax > rsi_filter:
            for j in range(l * 2):
                ma3 = []
                for k in range(3):

                    ma3.append(data_daily.iloc[currentday-j-k-1][4])
                ma3 = statistics.mean(ma3)
                          
                if j < int(l/2):
                    halfdata.append(ma3)

                if j >=l:
                    gaindata.append(ma3)
                else:

                    flagdata.append(ma3)
                    
            gain = max(gaindata) - min(gaindata)
            flag = max(flagdata) - min(flagdata)
               
            halfflag = max(halfdata) - min(halfdata) 

            value = gain - flag
                

            zdata = []
            
            for i in range(zl):
                pushvalue = data_daily.iloc[currentday-i-1][2] - data_daily.iloc[currentday-i-1][3]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            if z > zfilter and z2 > z2filter:
                    
                log.daily(screenbar,z,"WFlag", dateToSearch,pmPrice,data_daily,currentday,timeframe) 
      
if __name__ == '__main__':
    

    

    
    timeframe = '5min'
    premarket = False


    replace_setups = True



    #forecast //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    if True or ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)) :
            Daily.runDaily()


    #backtest ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else:
            
        if replace_setups:
            if(os.path.exists("C:/Screener/data_csvs/setups.csv")):
                os.remove("C:/Screener/data_csvs/setups.csv")
            pd.DataFrame().to_csv(("C:/Screener/tmp/setups.csv"),  header=False)
        
        try:
            df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
            strdate = df.iloc[len(df)-1][0]
           
            startdate = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            print(f"starting from {startdate}")
            time.sleep(3)
        except:
            startdate = date(2008, 1, 1)
                
        sample = data.get('AAPL',timeframe,premarket)
        index = data.findex(sample,startdate)



        search = sample.iloc[index][0]

        while index < len(sample) - 50:

            search = sample.iloc[index][0]

            Daily.runDaily(search,timeframe)

            index += 1






        #day_count = 1000000000000000
           
        #for single_date in (startdate + timedelta(n) for n in range(day_count)):

            #print(f"////////////////////////////////////// {single_date} //////////////////////////////////////")
            #Daily.runDaily(str(single_date),timeframe)

           # if startdate > date.today():
              #  print("finished")
               #break
        
        