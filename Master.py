from Data import Data as data
from Daily import Daily as daily
from Intraday import Intraday as intraday
from Screen import Screen as screen
import datetime
import time 


tv = None
browser = None
while True:
    now = datetime.datetime.now()
   # print(now.hour)
    #print(now.minute)
    if(tv == None):
        tv = screen.logInScrapper()
    if(browser == None):
        browser = screen.startFirefoxSession()

    if now.hour == 4 and now.minute == 0:
        print("updating data")
        screen.runDailyScan()
        data.isDataUpdated(data)

    elif now.hour == 5 and now.minute == 0:
        print(daily,"screening daily")
        daily.runDaily("0")
    
    elif now.hour == 5 and now.minute == 30:
        while now.hour <= 12:
            print("screening intraday")
            tv, browser = intraday.runIntraday()
    else:

        print("waiting")
        time.sleep(57)



   

   







