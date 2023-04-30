
from UI4 import UI as ui
import pandas as pd




#get setups df
df = pd.read_feather(r"C:\Screener\tmp\setups.feather")

#filter out all setups wihtout an annotation
df = df[df['annotation'] != ""]

#calculate traits for each setup
df = df.reset_index()
length = len(df)




for i in range(length):

    ticker = df.iat[i,2]
    date = df.iat[i,1]
    traits = ui.traits(ticker,date)
    row = df.iloc[i]
    row = row.append(pd.Series(traits))
    df.loc[i] = row
    print(i/length * 100)

print(df)













