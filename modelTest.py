
import random
import pandas as pd
from Create import Create as create
import time
import sys, os
from tensorflow.keras.models import load_model
import mplfinance as mpf
from Data7 import Data as data
from matplotlib import pyplot as plt

class modelTest:
    def runRandomTicker(setuptype,thresh):
        print('testing with random')


        
        while True:
            arglist = []
            for _ in range(100):
                arglist.append([setuptype,thresh])

            data.pool(modelTest.testRandom,arglist)

    def testRandom(bar):
        setuptype = bar[0]
        thresh = bar[1]
        model = load_model('C:/Screener/setups/models/model_' + setuptype)
        tickers = pd.read_feather(r"C:\Screener\sync\full_ticker_list.feather")['Ticker'].to_list()
        while True:
            try:
                ticker = tickers[random.randint(0,len(tickers)-1)]

                tickerdf = data.get(ticker)
                if(len(tickerdf) > 200):
                    date_list = tickerdf.index.to_list()
                    date = date_list[random.randint(0,len(date_list) - 1)]
                    if(tickerdf.iloc[data.findex(tickerdf, date)]['volume'] > 250000):
                        df = create.test_data(ticker, date, setuptype)
                    
                        sys.stdout = open(os.devnull, 'w')
                        god = model.predict(df)

                        val = 0
                        if god[0][1] > thresh:
                            val = 1
                        sys.stdout = sys.__stdout__
                
                
               
                        if val == 1:
                           
                            df1 = data.get(ticker)


                            ind= data.findex(df1,date)

                            df1 = df1[ind-50:ind + 1]
                   
                            mc = mpf.make_marketcolors(up='g',down='r')
                            s  = mpf.make_mpf_style(marketcolors=mc)
            
                            mpf.plot(df1, type='candle', volume=True  , 
 
                            style=s, warn_too_much_data=100000,returnfig = True, panel_ratios = (5,1), 
                            tight_layout = True,
                            vlines=dict(vlines = [date])
                            #colors = colorlist, alpha = .2,linewidths=1),
                                )      
                            plt.show()

                   
            except (ValueError, FileNotFoundError, TimeoutError, TypeError):
                print('Error')




    def runTestData(setuptype):

        model = load_model('C:/Screener/setups/models/model_'+ setuptype)
        setups = pd.read_feather('C:/Screener/setups/database/Testdata_' + setuptype + '.feather')
       
        right = 0
        total = 0

        while True:


            try:
                setup = setups.iloc[(random.randint(0,len(setups)-1))]
 

                ticker = setup['ticker'] 
                date =  setup['date']
                typee = setup["setup"]
    
                df = create.test_data(ticker,date, setuptype)


                sys.stdout = open(os.devnull, 'w')
                god = model.predict(df)

                val = 0
                
                if god[0][1] > god[0][0]:
                    val = 1

                sys.stdout = sys.__stdout__
            

                if typee == setuptype:
                    actual = 1
                else:
                    actual = 0


                if val == actual:
                    right += 1





                total += 1
                print(f'God 0: {str(god[0][0])} God 1: {str(god[0][1])}')
                print(f"{val} Actual: {typee}")
                #if val == 1 or typee == 1:
                if True:
                    df1 = data.get(ticker)


                    ind= data.findex(df1,date)

                    df1 = df1[ind-100:ind + 1]
                    mc = mpf.make_marketcolors(up='g',down='r')
                    s  = mpf.make_mpf_style(marketcolors=mc)
            
                    mpf.plot(df1, type='candle', volume=True  , 
 
                    style=s, warn_too_much_data=100000,returnfig = True, panel_ratios = (5,1), 
                    tight_layout = True
                     #  vlines=dict(vlines=[date])
                    #colors = colorlist, alpha = .2,linewidths=1),
                    )
                
        
                    plt.show()



            except (TypeError, ValueError, IndexError):
                print('Error')
    def combine(new,setuptype): 
        if new:
            setups = ['EP', 'NEP' , 'P','NP' , 'MR' , 'F' , 'NF']
            for setup in setups:
                df1 = pd.read_feather(f"C:/Screener/sync/database/ben_{setup}.feather")
                df2 = pd.read_feather(f"C:/Screener/sync/database/aj_{setup}.feather")
                df4 = pd.read_feather(f"C:/Screener/sync/database/laptop_{setup}.feather")
                df3 = pd.concat([df1, df2, df4]).reset_index(drop = True)
    
                df3.to_feather(f"C:/Screener/setups/database/{setup}.feather")
        else:
            df = pd.read_feather(r"C:/Screener/sync/allsetups.feather").sample(frac = .2)

            new_df = df.drop(axis=1, labels=["Z", "timeframe", "annotation"])
            for i in range(len(df)):
                new_df.at[i, 'ticker'] = df.iloc[i]['Ticker']
                new_df.at[i, 'date'] = df.iloc[i]['Date']
                if(df.iloc[i]['Setup'] == setuptype):
                    new_df.at[i, 'setup'] = 1
                else:
                    new_df.at[i, 'setup'] = 0
            new_df = new_df.drop(axis=1, labels=['Ticker', 'Date', 'Setup']).reset_index(drop = True)
            
        

            new_df.to_feather('C:/Screener/setups/database/' + setuptype + '.feather')

        




if __name__ == "__main__":
    setuptype = 'P'
    prcnt_setup = .35
    thresh = .85

    new = False
    #modelTest.combine(new,setuptype)
    #create.run(setuptype,prcnt_setup,True)
    modelTest.runRandomTicker(setuptype,thresh)
    #modelTest.runTestData(setuptype)








