from Daily import Daily as daily
from Intraday import Intraday as intraday
from Data import Data as data
import pandas as pd

dail = True

dat = False

if dat:
    data.isDataUpdated(data,pd.read_csv(r"C:\Screener\tmp\screener_data.csv"))

if dail:
   
    daily.runDaily(daily,"0")
    
else:
    intraday.runIntraday(intraday)