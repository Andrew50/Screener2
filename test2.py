
from Datav4 import Data as data

import pandas as pd



df = pd.read_csv(f"C:/Screener/data_csvs/AAPL_data.csv")



dfw= data.toWeekly(df)


print(dfw)