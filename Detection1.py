
import statistics
from Log3 import Log as log

from Data5 import Data as data

import pandas as pd

class Detection:

   

    def check(screenbar):
        
        try:
            


            date = screenbar[0]
            ticker = screenbar[1]
            tf = screenbar[2]
            path = screenbar[3]

            #print(f"{date} , {tf}, {ticker}")



            df = data.get(ticker,tf,date)




            if len(df) > 50:

             

                currentday = data.findex(df,date)

               
            
                dolVol, adr = Detection.requirements(df,currentday)

                
                
                

                if tf == 'd':
                    if dolVol > 1000000 and adr > 3:
                        sEP = True
                        sMR = True
                        sPivot = True
                        sFlag = True
                        dolVolFilter = 10000000
            
                        if(dolVol > .2* dolVolFilter  and adr > 3.5 and sEP):
                
                            Detection.EP(df,currentday, tf, ticker, path)
                        if(dolVol > .8 * dolVolFilter    and adr > 5 and sMR):
                            Detection.MR(df,currentday, tf, ticker, path)
                        if(dolVol > 1* dolVolFilter   and adr > 3.5 and sPivot):
                            Detection.Pivot(df,currentday, tf, ticker, path)
                        if(dolVol > .8 * dolVolFilter   and adr > 4 and sFlag):
                            Detection.Flag(df,currentday, tf, ticker, path)

            
                if tf == '1min':
                    z = 0
                    log.log(df,currentday, tf, ticker, z, path , 'Intraday') 
                if tf == '5min':
                    pass
                if tf == 'h':
                        
                    pass
            
        except FileNotFoundError: 
            pass
            #print(f"{ticker} is delisted")
        except pd.errors.EmptyDataError:
            pass
            #print('{ticker} is empty')
        except:
            pass
            #print(f"{ticker} failed")

     
        
    def requirements(df,currentday):

        try:
            
            
            if(currentday == None): 
               
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
           
            print('requirements failed')
            return 0 , 0



    def EP(df,currentday, tf, ticker, path):
        
       

        pmPrice = df.iloc[currentday][1]
        
        zfilter = 5.5
       
        
      
        prevClose = df.iloc[currentday-1][4]
        gaps = []
        lows = []
        highs = []
        todayGapValue = ((pmPrice/prevClose)-1)
        for j in range(20): 
            gaps.append((df.iloc[currentday-1-j][1]/df.iloc[currentday-2-j][4])-1)
            lows.append(df.iloc[currentday-j-1][3])
            highs.append(df.iloc[currentday-j-1][2])

        z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
           
        
        if(z > zfilter) and pmPrice > max(highs):
            log.log(df,currentday, tf, ticker, z, path, 'EP')  
            
        elif (z < -zfilter) and pmPrice < min(lows):
            log.log(df,currentday, tf, ticker, z, path , 'NEP')  

     
    
 
    def MR(df,currentday, tf, ticker, path):
        
        
        pmPrice = df.iloc[currentday][1]
        
        zfilter = 3.5
        gapzfilter0 = 5.5
        gapzfilter1 = 4
        changezfilter = 2.5
      
        prevClose = df.iloc[currentday-1][4]
        zdata = []
        zgaps = []
        zchange = []
            
        
        if df.iloc[currentday-1][4] < df.iloc[currentday-1][1] and df.iloc[currentday-2][4] < df.iloc[currentday-2][1] and df.iloc[currentday-3][4] < df.iloc[currentday-3][1]:

              
            for i in range(30):
                n = 29-i
                gapvalue = abs((df.iloc[currentday-n-1][1]/df.iloc[currentday-n-2][4]) - 1)
                changevalue = abs((df.iloc[currentday-n-1][4]/df.iloc[currentday-n-1][1]) - 1)
                lastCloses = 0
                    
                for c in range(4): 
                    
                    lastCloses += df.iloc[currentday-2-c-n][4]
                fourSMA = (lastCloses/4)
                datavalue = abs(fourSMA/df.iloc[currentday-n-1][1] - 1)
                if i == 29:
                    gapz1 = (gapvalue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                zgaps.append(gapvalue)
                zchange.append(changevalue)
                if i > 14:
                    zdata.append(datavalue)

             
            todayGapValue = abs((pmPrice/prevClose)-1)
            todayChangeValue = abs(df.iloc[currentday-1][4]/df.iloc[currentday-1][1] - 1)
            lastCloses = 0
            for c in range(4): 
                lastCloses = lastCloses + df.iloc[currentday-c-1][4]
                
            fourSMA = (lastCloses/4)
            value = (fourSMA)/pmPrice - 1


            
            gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
            changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
            z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
                
              
            if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value > 0):
              
               
                log.log(df,currentday, tf, ticker, z, path, 'MR')  
               
      
    def Pivot(df,currentday, tf, ticker, path):
       
       
        lowergapzfilter = 1.5
        lowergapzfilter2 = 1.5

        pmPrice = df.iloc[currentday][1]
       
        
        prevClose = df.iloc[currentday-1][4]
        zgaps = []
        for i in range(15):
            n = 14-i
            gapvalue = abs((df.iloc[currentday-n-1][1]/df.iloc[currentday-n-2][4]) - 1)
            zgaps.append(gapvalue)
            
        todayGapValue = (pmPrice/prevClose)-1
        gapz = (abs(todayGapValue)-statistics.mean(zgaps))/statistics.stdev(zgaps)
        lastCloses = 0
        for c in range(4): 
            lastCloses = lastCloses + df.iloc[currentday-c-1][4]
                
        ma3 = (lastCloses/4)
        close1 = df.iloc[currentday-1][4]
        close2 = df.iloc[currentday-2][4]
        open1 = df.iloc[currentday-1][1]
        open2 = df.iloc[currentday-2][1]
        low1 = df.iloc[currentday-1][3]
        high1 = df.iloc[currentday-1][2]
        z = gapz
        if gapz > lowergapzfilter and close1 < ma3  and close1 < close2 and close2 < open2 and close1 < open1 and open1 < close2 and pmPrice > high1 :
                
                
           log.log(df,currentday, tf, ticker, z, path, 'Pivot')   

        if gapz > lowergapzfilter2 and close1 > ma3  and close1 > close2 and close2 > open2 and close1 > open1 and open1 > close2 and pmPrice < low1:

            log.log(df,currentday, tf, ticker, z, path, 'Pivot')  
      


    def Flag(df,currentday, tf, ticker, path):

        pmPrice = df.iloc[currentday][1]
       
        
        #if test:
           # zfilter = 4
       # else:
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
                
                change = (df.iloc[currentday-k-j-1][4]/df.iloc[currentday-k-j-2][4]) - 1
                
                    
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

                    ma3.append(df.iloc[currentday-j-k-1][4])
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
                pushvalue = df.iloc[currentday-i-1][2] - df.iloc[currentday-i-1][3]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            
            if z > zfilter and z2 > z2filter:
                    
                log.log(df,currentday, tf, ticker, z, path, 'Flag')  

      

    def weeklyFlag(df,currentday, tf, ticker, path):
        pmPrice = df.iloc[currentday][1]
        
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
                change = (df.iloc[currentday-k-j-1][4]/df.iloc[currentday-k-j-2][4]) - 1
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

                    ma3.append(df.iloc[currentday-j-k-1][4])
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
                pushvalue = df.iloc[currentday-i-1][2] - df.iloc[currentday-i-1][3]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            if z > zfilter and z2 > z2filter:
                    
                log.log(df,currentday, tf, ticker, z, path, 'WWFlg')  