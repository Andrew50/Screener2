
from tvDatafeed import TvDatafeed
from Daily2 import Daily as daily
import datetime
from datetime import date, timedelta



start = 70 #



print(datetime.datetime.now())
start_date = date(2013, 1, 1)
day_count = 2500
for single_date in (start_date + timedelta(n) for n in range(day_count)):

    daily.runDaily(daily, str(single_date))


