
from UI4 import UI as ui
import pandas as pd
from Data7 import Data as data







def god (s):
    try:
        ticker = s[1]
        date = s[0]
        traits = ui.traits(ticker,date)
 
        row = s.append(pd.Series(traits))
        return row
    except:
        pass
 


if __name__ == '__main__':

    setup = "EP"
    size = 1000







    #get setups df
    df = pd.read_feather(r"C:\Screener\tmp\setups.feather")

    #filter out all setups wihtout an annotation
    #df = df[df['annotation'] != ""]
    df = df[df['Setup'] == setup]
    df = df.sample(size)
    #format shit
    df = df.reset_index(drop = True)
   
    
    #create list of series so that it can be multiprocessed
    container = []
    for index, row in df.iterrows():
        container.append(row)

    #calculate traits for each setup
    df = data.pool(god,container)

    #change list of series into df
    df = pd.DataFrame(df)

    #format column titles to str so that it can be worked with
    df.columns = df.columns.astype(str)
 



    #rename columns to descriptors
    df.rename(columns={'0':'gap',
                       '1':'adr',
                       '2':'vol',
                       '3':'q',
                       '4':'one',
                       '5':'two',
                       '6':'three',
                       '7':'ten',
                       '8':'time',
                       '9':'vol1'}, inplace = True)

    #replace qqq boolean with int
    df['q'].replace({False:0, True:1}, inplace = True)



    print(df)


    df.to_feather(r"C:\Screener\tmp\ml"+setup+".feather")



  













