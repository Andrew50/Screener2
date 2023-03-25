from Datav4 import Data as data
from Daily2 import Daily as daily
from IntradayV2 import Intraday as intraday
from Screen import Screen as screen
import datetime
import time 


tv = None
browser = None

if(tv == None):
        tv = screen.logInScrapper()
if(browser == None):
    browser = screen.startFirefoxSession()



while True:
    now = datetime.datetime.now()
   # print(now.hour)
    #print(now.minute)
    if now.hour == 5 and now.minute == 1:
        print("updating data")
        screen.runDailyScan(browser)

        data.isDataUpdated(tv)

    elif now.hour == 5 and now.minute == 15:
        print(daily,"screening daily")
        daily.runDaily(daily, "0")

    
    
    
    elif now.hour == 5 and now.minute == 30:
        while now.hour <= 12:
            screen.tryCloseLogout(browser)
            print("screening intraday")
            tv, browser = intraday.runIntraday(tv, browser)
    else:
        
        print("waiting")
        time.sleep(40)
        screen.tryCloseLogout(browser)

    if(tv == None):
        tv = screen.logInScrapper()
    if(browser == None):
        browser = screen.startFirefoxSession()



   

   






