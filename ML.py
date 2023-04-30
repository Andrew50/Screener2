
from UI4 import UI as ui
import pandas as pd
from Data7 import Data as data




#get setups df
df = pd.read_feather(r"C:\Screener\tmp\setups.feather")

#filter out all setups wihtout an annotation
df = df[df['annotation'] != ""]

#calculate traits for each setup
df = df.reset_index()
length = len(df)


container = []



def god (s):
    ticker = s[2]
    date = s[1]
    traits = ui.traits(ticker,date)
 
    row = s.append(pd.Series(traits))
    return row
 






for index, row in df.iterrows():
    container.append(row)


df = data.pool(god,container)




print(df)













