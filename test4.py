import pandas as pd



setup = 'P'

df1 = pd.read_feather('C:/Screener/setups/aj' + setup + '.feather')


df2 = pd.read_feather('C:/Screener/setups/ben' + setup + '.feather')



df3 = pd.concat([df1,df2]).reset_index(drop= True)

print(df3)

df4 = df3[df3['setup'] == 1]

print(df4)

df3.to_feather('C:/Screener/setups/' + setup + '.feather')