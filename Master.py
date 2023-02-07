import dataclasses
import pandas as pd
from Data import Data as data
from Daily import Daily as daily
from Intraday import Intraday as intraday
from Screen import Screen as screen
import schedule
import time



while True:
    now = datetime.now()

    if now.hour == 4 and now.minute == 0:
        screen.Daily
        data.isDataUpdated

    if now.hour == 5 and now.minute == 0:
        daily.Daily
    
    if now.hour == 5 and now.minute == 31:
        while now.hour <= 12:
            intraday.Intraday
    

   

   







