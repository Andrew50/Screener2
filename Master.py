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

    if now.hour == 4 and now.minute == 00:
        print("updating data")
        screen.runDailyScan(browser)

        data.isDataUpdated(tv)

    elif now.hour == 4 and now.minute == 59:
        print(daily,"screening daily")
        daily.runDaily(daily, "0",True)
    
    elif now.hour == 7 and now.minute == 2:
        while now.hour <= 12:
            screen.tryCloseLogout(browser)
            print("screening intraday")
            tv, browser = intraday.runIntraday(tv, browser)
    else:

        print("waiting")
        time.sleep(40)



   

   







