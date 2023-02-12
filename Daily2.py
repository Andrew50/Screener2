import os 
import pandas as pd
import statistics
import math
import datetime
from discordManager import discordManager as dM
import warnings
from pathos.multiprocessing import ProcessingPool as Pool
warnings.filterwarnings("ignore")
class Daily:

    def sfindIndex(df, dateTo):
        if dateTo == "0":
            return len(df)
        lookforSplit = dateTo.split("-")
        middle = int(len(df)/2)
        middleDTOD = str(df.iloc[middle]['datetime'])
        middleSplit = middleDTOD.split("-")      
        yearDifference = int(middleSplit[0]) - int(lookforSplit[0])
        monthDifference = int(middleSplit[1]) - int(lookforSplit[1])
        if(monthDifference < 0):
            yearDifference = yearDifference + 1
            monthDifference = -12 + monthDifference
        addInt = (yearDifference*-252) + (monthDifference*-21)
        newRef = middle + addInt
        dateTo = dateTo + " 05:30:00"
        if(newRef < 0):
            return 99999
        if( ((len(df) - newRef) < 20) or (newRef > len(df))):
            for i in range(35):
                dateTimeofDayAhead = str(df.iloc[len(df)-35 + i]['datetime'])
                if(dateTimeofDayAhead == dateTo):
                    return int(2065 + i)
        else:
            for i in range(35):
                dateTimeofDayBehind = str(df.iloc[newRef - i]['datetime'])
                if(dateTimeofDayBehind == dateTo):
                    return (newRef - i)
                dateTimeofDayAhead = str(df.iloc[newRef + i]['datetime'])
                if(dateTimeofDayAhead == dateTo):
                    return (newRef + i)
        return 99999


    def processTickers(sbr):
        sMR = False
        sEP = True
        sPivot = True
        sFlag = False
        chartSize = 80
        rightbuffer = 20
        screenbar = sbr
        tick = str(screenbar['Ticker'])
        dateToSearch = screenbar['dateToSearch']
        print(tick)
        if (os.path.exists("C:/Screener/data_csvs/" + tick + "_data.csv")):
            data_daily_full = pd.read_csv(f"C:/Screener/data_csvs/{tick}_data.csv")
        
            if len(data_daily_full) > 50:
                   
                indexOfDay = Daily.sfindIndex(data_daily_full, dateToSearch)
                if(indexOfDay != 99999):
                        
                    if (dateToSearch == "0"):
                        prevClose = screenbar['Price']
                            
                        pmChange = screenbar['Pre-market Change']
            
                        dolVol = screenbar['Volume*Price']
                        pmPrice = prevClose + pmChange                 
                    else:
                        pmPrice = data_daily_full.iloc[indexOfDay][2]#open
                        prevClose = data_daily_full.iloc[indexOfDay-1][5] #close
                        dolVol = prevClose*data_daily_full.iloc[indexOfDay-1][6]
                        pmChange = pmPrice/prevClose - 1
    
                    rightedge = indexOfDay + 1
                    data_daily = data_daily_full[(rightedge - chartSize):(rightedge)]
                    currentday = chartSize-1

                        #pmPrice = data_daily_full.iloc[indexOfDay][2]#open
                        #prevClose = data_daily_full.iloc[indexOfDay-1][5] #close
                        #if len(data_daily_full) - indexOfDay > rightbuffer:
                        #    rightedge = indexOfDay+rightbuffer
                        #    currentday = chartSize-rightbuffer
                        #else:
                            #  rightedge = len(data_daily_full)
                            #  currentday = chartSize-(rightedge - indexOfDay)
                        
                    #data_daily = data_daily_full[(rightedge - chartSize ):(rightedge)]
                    data_daily['Datetime'] = pd.to_datetime(data_daily['datetime'])
                    data_daily = data_daily.set_index('Datetime')
                    data_daily = data_daily.drop(['datetime'], axis=1)
                    #print(indexOfDay)
                    #print(len(data_daily_full))
                    #print(currentday)
                    #print(len(data_daily))
                    if(dolVol > 1000000  and prevClose > 3 and sEP):
                        Daily.EP(data_daily, currentday, pmPrice, prevClose,screenbar, dateToSearch)
                    if(dolVol > 5000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sMR):
                        Daily.MR(data_daily, currentday, pmPrice, prevClose,screenbar, dateToSearch)
                    if(dolVol > 15000000  and prevClose > 2 and pmChange != 0 and math.isnan(pmChange) != True and sPivot):
                        Daily.Pivot(data_daily, currentday, pmPrice, prevClose,screenbar, dateToSearch)
    def runDaily(self, dateToSearch,algl):
        if algl:
            sMR = True
            sEP = True
            sPivot = True
            sFlag = True
        else:
            sMR = True
            sEP = True
            sPivot = True
            sFlag = False
        dateSplit = dateToSearch.split("-")
        x_date = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
        if(x_date.weekday() >= 5):
            print("The date given is not a weekday.")
            return False

        if (dateToSearch == "0"):
            screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        else:
            screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        screenbars = []
        for i in range(len(screener_data)):
            screener_data.at[i, 'dateToSearch'] = dateToSearch
            screenbars.append(screener_data.iloc[i])
        with Pool(nodes=7) as pool:
            pool.map(Daily.processTickers, screenbars)
            

    #currentday is the day of the setup. This would be the day that the setup would be bough
    #if datetosearch is 0 then currentday is the length of daily_data


    def EP(data_daily, currentday, pmPrice, prevClose, screenbar, dateToSearch):
        
        zfilter = 7
        
        try: 
            gaps = []
            lows = []
            highs = []
            todayGapValue = round(((pmPrice/prevClose)-1), 2)
            for j in range(20): 
                gaps.append((data_daily.iloc[currentday-1-j][1]/data_daily.iloc[currentday-2-j][4])-1)
                lows.append(data_daily.iloc[currentday-j-1][3])
                highs.append(data_daily.iloc[currentday-j-1][2])
            z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
            
            if(z > zfilter) and pmPrice > max(highs):
                dM.post(data_daily,screenbar,z,"EP", dateToSearch) 
                
            elif (z < -zfilter) and pmPrice < min(lows):
                dM.post(data_daily,screenbar,z,"NEP", dateToSearch) 
                #print("1")
            #dM.post(data_daily,screenbar,z,"NEP",currentday)
        except IndexError:
            print("index error")
        except TimeoutError:
            print("timeout error")
        except FileNotFoundError:
            print("file error") 
 
    def MR(data_daily, currentday,pmPrice,prevClose,screenbar, dateToSearch):
        #print(currentday)
        #print(len(data_daily))
        
        zfilter = 3.3
        gapzfilter0 = 8
        gapzfilter1 = 3.5
        changezfilter = 3.2
        try: 
            zdata = []
            zgaps = []
            zchange = []
            
            
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
            gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
            changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
            lastCloses = 0
            closes = []
            for c in range(4): 
                lastCloses = lastCloses + data_daily.iloc[currentday-c-1][4]
                
            fourSMA = (lastCloses/4)
            value = (fourSMA)/pmPrice - 1
            
            z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
            #print(f"{z, gapz, gapz1, changez}") #z debugger
            #print("historical" + f"{datavalue, gapvalue,changevalue}") #historical debugger
           # print("current" + f"{value,todayGapValue ,todayChangeValue}") #current debugger
            #print(z,gapz, gapz1, changez)
            #print("change data" +f"{ statistics.mean(zchange), statistics.stdev(zchange) }")
            if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value > 0):
                #print(data_daily)
               
                dM.post(data_daily,screenbar,z,"MR", dateToSearch) 
                #print(f"{tick, data_daily.index[len(data_daily)-1], z, abs(value), statistics.mean(zdata),statistics.stdev(zdata), pmPrice, fourSMA}")
               # print(f"{tick,closes}")
            
        #except IndexError:
         #  print(" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")
            
    def Pivot(data_daily, currentday,pmPrice,prevClose,screenbar, dateToSearch):
        
        zfilter = 5
        changezfilter = 4
        gapzfilter = 8

        try: 
            zdata = []
            zgaps = []
            zchange = []
            
            for i in range(30):
                n = 29-i
                gapvalue = abs((data_daily.iloc[currentday-n-1][1]/data_daily.iloc[currentday-n-2][4]) - 1)
                changevalue = abs((data_daily.iloc[currentday-n-1][4]/data_daily.iloc[currentday-n-1][1]) - 1)
                lastCloses = 0
                    
                for c in range(3): 
                    
                    lastCloses += data_daily.iloc[currentday-3-c-n][4]
                fourSMA = (lastCloses/3)
                datavalue = abs(fourSMA/data_daily.iloc[currentday-n-2][4] - 1)
                zgaps.append(gapvalue)
                zchange.append(changevalue)
                if i > 14:
                    zdata.append(datavalue)


            todayGapValue = (pmPrice/prevClose)-1
            todayChangeValue = abs(data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1)
            gapz = (abs(todayGapValue)-statistics.mean(zgaps))/statistics.stdev(zgaps)
            changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
            lastCloses = 0
            closes = []
            for c in range(3): 
                lastCloses = lastCloses + data_daily.iloc[currentday-c-2][4]
                closes.append(data_daily.iloc[currentday-c-2][4])
            fourSMA = (lastCloses/3)
            value = (fourSMA)/data_daily.iloc[currentday-1][4] - 1
            #print(data_daily)
            #print(f"{tick, closes }")
            #print(data_daily.iloc[currentday-1][4] - 1)
            z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
            #print(f"{z, gapz, gapz1, changez}") #z debugger
            #print("historical" + f"{datavalue, gapvalue,changevalue}") #historical debugger
            #print("current" + f"{value,todayGapValue ,todayChangeValue}") #current debugger
            #print(z,gapz, gapz1, changez)
            #print("change data" +f"{ statistics.mean(zchange), statistics.stdev(zchange) }")

            z2 = z*gapz
            #print(z2)
            if z2 > zfilter and value > 0 and todayGapValue > 0 and changez < changezfilter and gapz < gapzfilter:
                #print(data_daily)
                
                dM.post(data_daily,screenbar,z2,"Pivot", dateToSearch) 
                #print(f"{tick, data_daily.index[len(data_daily)-1], z, abs(value), statistics.mean(zdata),statistics.stdev(zdata), pmPrice, fourSMA}")
               # print(f"{tick,closes}")

            if z2 < -zfilter and value < 0 and todayGapValue < 0 and changez < changezfilter and gapz < gapzfilter:
                dM.post(data_daily,screenbar,z2,"Pivot", dateToSearch) 
            
        except IndexError:
           print(" did not exist at the date " )
        except TimeoutError:
            print("Timeout caught")
        except FileNotFoundError:
            print(" does not have a file")

if __name__ == '__main__':
    print(datetime.datetime.now())
    Daily.runDaily(Daily, '2020-09-22',False)
    print(datetime.datetime.now())
