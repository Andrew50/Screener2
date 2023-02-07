from Data import Data as data
from Daily import Daily as daily
from Intraday import Intraday as intraday
from Screen import Screen as screen
import datetime



while True:
    now = datetime.datetime.now()

    if now.hour == 4 and now.minute == 0:
        print("updating data")
        screen.Daily(screen)
        data.isDataUpdated(data)

    if now.hour == 5 and now.minute == 0:
        print(daily,"screening daily")
        daily.runDaily("0")
    
    if now.hour == 5 and now.minute == 31:
        while now.hour <= 12:
            print("screening intraday")
            intraday.Intraday
    

   

   







