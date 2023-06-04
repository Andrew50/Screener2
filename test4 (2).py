import pandas as pd




class Test4:

    def run():
        df = pd.read_feather(r"C:/Screener/sync/allsetups.feather")

        new_df = df.drop(axis=1, labels=["Z", "timeframe", "annotation"])
        for i in range(len(df)):
            new_df.at[i, 'ticker'] = df.iloc[i]['Ticker']
            new_df.at[i, 'date'] = df.iloc[i]['Date']
            if(df.iloc[i]['Setup'] == 'EP'):
                new_df.at[i, 'setup'] = 1
            else:
                new_df.at[i, 'setup'] = 0
        new_df = new_df.drop(axis=1, labels=['Ticker', 'Date', 'Setup'])

        new_df.to_feather('C:/Screener/setups/database/EP.feather')

        print(new_df)
    '''
    def merge():
        setups = ["EP", "F", "FB", "MR", "NEP", "NF", "NFB", "NP", "P"]
        for setup in setups:
            df1 = pd.read_feather(f"C:/Screener/setups/{setup}.feather")
            df2 = pd.read_feather(f"C:/Screener/setups/combine/{setup}.feather")
            df3 = pd.concat([df1, df2]).reset_index(drop = True)
            print(df3)
            df3.to_feather(f"C:/Screener/setups/{setup}.feather")
            '''
'''
df3 = pd.concat([df1,df2]).reset_index(drop= True)

print(df3)

df4 = df3[df3['setup'] == 1]

print(df4)

df3.to_feather('C:/Screener/setups/' + setup + '.feather')
'''



if __name__ == '__main__':
    Test4.run()