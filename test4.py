import pandas as pd



setups = ["EP", "F", "FB", "MR", "NEP", "NF", "NFB", "NP", "P"]

for setup in setups:
    df = pd.read_feather(f"C:/Screener/setups/{setup}.feather")
    rows = []
    for i in range(len(df)):
        if(df.iloc[i]['ticker'] == "BKSY"):
            rows.append(i)
    print(rows)
    df = df.drop(labels=rows)
    df.to_feather(f"C:/Screener/setups/{setup}.feather")


'''
df3 = pd.concat([df1,df2]).reset_index(drop= True)

print(df3)

df4 = df3[df3['setup'] == 1]

print(df4)

df3.to_feather('C:/Screener/setups/' + setup + '.feather')
'''