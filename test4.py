import pandas as pd




class Test4:
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
    Test4.merge()