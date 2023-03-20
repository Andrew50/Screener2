
import statistics
from Log2 import log as log


class Detection:



    def check(dolVol, adr,df, currentday, pmPrice,screenbar, dateToSearch,timeframe )


    def EP(data_daily, currentday, pmPrice = df.iloc[currentday][1], screenbar, dateToSearch,timeframe):
      
        
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

    
 
    def MR(data_daily, currentday,pmPrice = df.iloc[currentday][1],screenbar, dateToSearch,timeframe):
        
    
        
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