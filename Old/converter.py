
import pandas as pd

from Data7 import Data as data

import datetime
from pyarrow import feather









class Con:
   
        
        
        '''
        
        try:
            df = feather.read_feather(r"C:/Screener/feather_minute/" + ticker + ".feather")
            df['datetime'] = pd.to_datetime(df['datetime'])
            #print(type(df.iloc[0]['datetime']))
            df = df.set_index('datetime')
            
            feather.write_feather(df,"C:/Screener/minute/" + ticker + ".feather")
        except:
            pass
        '''



if __name__ == "__main__":
    #l = pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")['Ticker'].tolist()

    #print(pd.read_feather(r"C:\Screener\tmp\setups.feather"))
    
    


    df = pd.read_csv('C:/Screener/tmp/full_ticker_list - backup.csv')
    df.to_feather('C:/Screener/tmp/full_ticker_list.feather')


    

    '''
   


    df = pd.DataFrame({'datetime':[datetime.datetime.now(),datetime.datetime.now()],
                       'god':['god', 'gosh']})
        
        
    feather.write_feather(df,"C:/Screener/god.feather")
    df1 = feather.read_feather(r"C:/Screener/god.feather")
    print(type(df1.iloc[0][0]))

    df.to_csv("C:/Screener/god.feather")
    df2 = pd.read_csv("C:/Screener/god.feather")

    print(type(df2.iloc[0][0]))
    
    '''
    