
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
    size = 500







    #get setups df
    df = pd.read_feather(r"C:\Screener\sync\setups.feather")

    #filter out all setups wihtout an annotation
    #df = df[df['annotation'] != ""]
    df = df[df['Setup'] == setup]
    df = df.sample(size).reset_index(drop = True)
    #format shit
    newdf = df[['Ticker', 'Date']]
    for i in range(len(newdf)):
        newdf.at[i, 'setup'] = 1
    newdf = newdf.rename({'Ticker':'ticker', 'Date':'date'}, axis=1)


    sets = pd.read_feather(r"C:\Screener\sync\setups.feather")
    test = sets[sets['Setup'] != "EP"]
    test = test.sample(size).reset_index(drop = True)
    nnn = test[['Ticker', 'Date']]
    for j in range(len(nnn)):
        nnn.at[j, 'setup'] = 0

    nnn = nnn.rename({'Ticker':'ticker', 'Date':'date'}, axis=1)
    print(nnn)
    newdd = pd.concat([newdf, nnn]).reset_index(drop = True)
    newdd['date'] = pd.to_datetime(newdd['date'])
    print(newdd.to_string())

   
    '''
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

    '''
    


    newdd.to_feather(r"C:\Screener\setups\EP.feather")



  













