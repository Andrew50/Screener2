
from Data5 import Data as data
import datetime
import yfinance as yf



class RRTest: 

    def getDateDf(df, date): 
        openTime = datetime.time(9,30,0)
        openT = datetime.datetime.combine(date, openTime) 
        startIndex = data.findex(df, openT)
        closeTime = datetime.time(15,55,0)
        closeT = datetime.datetime.combine(date, closeTime)
        endIndex = data.findex(df, closeT)
        newDf = df[startIndex:endIndex+1]

        return newDf

if __name__ == "__main__":
    lap = (datetime.datetime.now())


    df = data.get("RIVN",'5min')
    #yFin = yf.download("AAPL", start="2023-03-10", interval="1m")
    date = datetime.datetime(2023, 2, 6)
    #date = datetime.datetime(2023, 2, 6)
    #print(datetime.datetime.now() - lap)
    lap = (datetime.datetime.now())
    index = data.findex(df,date)
    print(datetime.datetime.now() - lap)

    #print(str(date.date()) + " werwerwerew")
    #print(df[20000:20050])
    #print(df.iloc[index]['datetime'])
    #print(df.iloc[index+1]['datetime'])
    print(RRTest.getDateDf(df, date))

    ## FIVE MIN FADE