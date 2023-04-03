
import statistics
from Log3 import Log as log

from Data7 import Data as data

import pandas as pd
import datetime
from tqdm import tqdm

class Detection:

   

    def check(bar):
        
        ticker = bar[0]
        tf = bar[1]
        path = bar[2]
        date_list = bar[3]
        date = date_list[0]
        try:
            df = data.get(ticker,tf,date)
        except FileNotFoundError:
            return
        except TypeError:
            return
        
        for date in date_list:
            try:
                if len(df) > 50:
                    
                    currentday = data.findex(df,date)
                    if currentday != None:
                        length = 500
                        df = df[currentday-length:currentday + 50]
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
                            
                            if dolVol > 20000 and adr > .08:
                            
                                Detection.Pop(df,currentday, tf, ticker, path)
                            
                    
                        if tf == '5min':
                            if dolVol > 100000 and adr > .1:
                                Detection.Pop(df,currentday, tf, ticker, path)
                    
                        if tf == 'h':
                        
                            pass
            
            except:
                pass

        #except Exception as e: print(e)
  
    def requirements(df,currentday):

        dol_vol_l = 5
        adr_l = 15

        try:
            if(currentday == None): 
                return 0, 0
            dolVol = []
            for i in range(dol_vol_l):
                dolVol.append(df.iat[currentday-1-i,3]*df.iat[currentday-1-i,4])
            dolVol = statistics.mean(dolVol)              
            adr= []
            for j in range(adr_l): 
                high = df.iat[currentday-j-1,1]
                low = df.iat[currentday-j-1,2]
                val = (high/low - 1) * 100
                adr.append(val)
            adr = statistics.mean(adr)  
            return dolVol, adr
        except:
            return 0 ,0
           
    def Pop(df,currentday, tf, ticker, path):
        
        i = 0
        zfilter = 25
       
        data = []
        length = 500

        x = df.iat[currentday - i,4] + df.iat[currentday - i-1,4]
        y = ((df.iat[currentday - i,3]/df.iat[currentday - i,0]) + (df.iat[currentday - i,3]/df.iat[currentday - i,0]) - 2)
       
        current_value = x*pow(y,2)
        

        '''
        
        for i in range(length): 
            x = df.iat[currentday - i-1,4] + df.iat[currentday - i-2,4]
            y = ((df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) + (df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) - 2)
            value = x*pow(y,2)
            data.append(value)

'''

        '''
        for i in range(length): 
            x = df.iat[currentday - i-1, 4] + df.iat[currentday - i-2,4]
            y = ((df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) + (df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) - 2)
            value = x*pow(y,2)
            data.append(value)

    '''
       # print(f'{len(df)} , {currentday}')
      
        df = df[currentday-length:currentday + 1]
    
        currentday = length - 1
    
        for i in range(length): 
            x = df.iat[currentday - i-1, 4] + df.iat[currentday - i-2,4]
            y = ((df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) + (df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) - 2)
            value = x*pow(y,2)
            data.append(value)
    
        
        z = (current_value - statistics.mean(data))/statistics.stdev(data)
    
        if ((z < -zfilter) or (z > zfilter)):
        
            log.log(df,currentday, tf, ticker, z, path , 'Pop')  
            


    def EP(df,currentday, tf, ticker, path):
        pmPrice = df.iat[currentday,0]
        
        zfilter = 5.5

        prevClose = df.iat[currentday-1,3]
        gaps = []
        lows = []
        highs = []
        todayGapValue = ((pmPrice/prevClose)-1)
        for j in range(20): 
            gaps.append((df.iat[currentday-1-j,0]/df.iat[currentday-2-j,3])-1)
            lows.append(df.iat[currentday-j-1,2])
            highs.append(df.iat[currentday-j-1,1])

        z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
           
        
        if(z > zfilter) and pmPrice > max(highs):
            log.log(df,currentday, tf, ticker, z, path, 'EP')  
            
        elif (z < -zfilter) and pmPrice < min(lows):
            log.log(df,currentday, tf, ticker, z, path , 'NEP')  

 
    def MR(df,currentday, tf, ticker, path):
        
        
        pmPrice = df.iat[currentday,0]
        
        zfilter = 3.5
        gapzfilter0 = 5.5
        gapzfilter1 = 4
        changezfilter = 2.5
      
        prevClose = df.iat[currentday-1,3]
        zdata = []
        zgaps = []
        zchange = []
            
        
        if df.iat[currentday-1,3] < df.iat[currentday-1,0] and df.iat[currentday-2,3] < df.iat[currentday-2,0] and df.iat[currentday-3,3] < df.iat[currentday-3,0]:

              
            for i in range(30):
                n = 29-i
                gapvalue = abs((df.iat[currentday-n-1,0]/df.iat[currentday-n-2,3]) - 1)
                changevalue = abs((df.iat[currentday-n-1,3]/df.iat[currentday-n-1,0]) - 1)
                lastCloses = 0
                    
                for c in range(4): 
                    
                    lastCloses += df.iat[currentday-2-c-n,3]
                fourSMA = (lastCloses/4)
                datavalue = abs(fourSMA/df.iat[currentday-n-1,0] - 1)
                if i == 29:
                    gapz1 = (gapvalue-statistics.mean(zgaps))/statistics.stdev(zgaps)
                zgaps.append(gapvalue)
                zchange.append(changevalue)
                if i > 14:
                    zdata.append(datavalue)

             
            todayGapValue = abs((pmPrice/prevClose)-1)
            todayChangeValue = abs(df.iat[currentday-1,3]/df.iat[currentday-1,0] - 1)
            lastCloses = 0
            for c in range(4): 
                lastCloses = lastCloses + df.iat[currentday-c-1,3]
                
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

        pmPrice = df.iat[currentday,0]
       
        
        prevClose = df.iat[currentday-1,3]
        zgaps = []
        for i in range(15):
            n = 14-i
            gapvalue = abs((df.iat[currentday-n-1,0]/df.iat[currentday-n-2,3]) - 1)
            zgaps.append(gapvalue)
            
        todayGapValue = (pmPrice/prevClose)-1
        gapz = (abs(todayGapValue)-statistics.mean(zgaps))/statistics.stdev(zgaps)
        lastCloses = 0
        for c in range(4): 
            lastCloses = lastCloses + df.iat[currentday-c-1,3]
                
        ma3 = (lastCloses/4)
        close1 = df.iat[currentday-1,3]
        close2 = df.iat[currentday-2,3]
        open1 = df.iat[currentday-1,0]
        open2 = df.iat[currentday-2,0]
        low1 = df.iat[currentday-1,2]
        high1 = df.iat[currentday-1,1]
        z = gapz
        if gapz > lowergapzfilter and close1 < ma3  and close1 < close2 and close2 < open2 and close1 < open1 and open1 < close2 and pmPrice > high1 :
                
                
           log.log(df,currentday, tf, ticker, z, path, 'Pivot')   

        if gapz > lowergapzfilter2 and close1 > ma3  and close1 > close2 and close2 > open2 and close1 > open1 and open1 > close2 and pmPrice < low1:

            log.log(df,currentday, tf, ticker, z, path, 'Pivot')  
      


    def Flag(df,currentday, tf, ticker, path):

        pmPrice = df.iat[currentday,0]
       
        
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
                
                change = (df.iat[currentday-k-j-1,3]/df.iat[currentday-k-j-2,3]) - 1
                
                    
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

                    ma3.append(df.iat[currentday-j-k-1,3])
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
                pushvalue = df.iat[currentday-i-1,1] - df.iat[currentday-i-1,2]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            
            if z > zfilter and z2 > z2filter:
                    
                log.log(df,currentday, tf, ticker, z, path, 'Flag')  

      

    def weeklyFlag(df,currentday, tf, ticker, path):
        pmPrice = df.iat[currentday,0]
        
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
                change = (df.iat[currentday-k-j-1,3]/df.iat[currentday-k-j-2,3]) - 1
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

                    ma3.append(df.iat[currentday-j-k-1,3])
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
                pushvalue = df.iat[currentday-i-1,1] - df.iat[currentday-i-1,2]
                zdata.append(pushvalue)

            z = (value - statistics.mean(zdata))/statistics.stdev(zdata)
            z2 =  -((halfflag - statistics.mean(zdata))/statistics.stdev(zdata))
             
            if z > zfilter and z2 > z2filter:
                    
                log.log(df,currentday, tf, ticker, z, path, 'WWFlg')  
