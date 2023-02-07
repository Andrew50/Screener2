from Daily import Daily as daily
from Intraday import Intraday as intraday


dail = True


if dail:
   
    daily.runDaily(daily,'2022-02-24')
    
else:
    intraday.Intraday(intraday)