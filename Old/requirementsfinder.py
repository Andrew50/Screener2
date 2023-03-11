import os 
import pandas as pd
from Datav4 import Data as datas
import statistics



screener_data = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")

numTickers = len(screener_data)

dateToSearch = '2023-01-03'

data = []


for i in range(numTickers):
    screenbar = screener_data.iloc[i]
    tick = str(screenbar['Ticker'])
    if (os.path.exists("C:/Screener/data_csvs/" + tick + "_data.csv")):
        data_daily = pd.read_csv(f"C:/Screener/data_csvs/{tick}_data.csv")
        
        
                   
        indexOfDay = datas.findIndex(data_daily, dateToSearch,False)
        if(indexOfDay != 99999):
            dolVol = []
            for i in range(20):
                dolVol.append(data_daily.iloc[indexOfDay-1-i][4]*data_daily.iloc[indexOfDay-1-i][5])
            dolVol = statistics.mean(dolVol)
            if dolVol == dolVol:
                data.append(dolVol)
                





print(statistics.mean(data))
print(statistics.stdev(data))
