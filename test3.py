

import random
import pandas as pd
from Create import Create as create
import time
import sys, os
from tensorflow.keras.models import load_model
import mplfinance as mpf
from Data7 import Data as data
from matplotlib import pyplot as plt

class Test3:
    def runRandomTicker(setuptype):
        model = load_model('model_' + setuptype)
        tickers = pd.read_feather(r"C:\Screener\sync\full_ticker_list.feather")['Ticker'].to_list()
        while True:
            try:
                ticker = tickers[random.randint(0,len(tickers)-1)]

                tickerdf = data.get(ticker)
                date_list = tickerdf.index.to_list()
                date = date_list[random.randint(0,len(date_list) - 1)]
                df = create.test_data(ticker, date)
                sys.stdout = open(os.devnull, 'w')
                god = model.predict(df)

                val = 0
                if god[0][1] > 0.2:
                    val = 1
                sys.stdout = sys.__stdout__
                print(f'God 0: {str(god[0][0])} God 1: {str(god[0][1])}')
                print(f"{val}")
                if val == 1:
                        df1 = data.get(ticker)


                        ind= data.findex(df1,date)

                        df1 = df1[ind-100:ind + 1]
                        mc = mpf.make_marketcolors(up='g',down='r')
                        s  = mpf.make_mpf_style(marketcolors=mc)
            
                        mpf.plot(df1, type='candle', volume=True  , 
 
                        style=s, warn_too_much_data=100000,returnfig = True, panel_ratios = (5,1), 
                        tight_layout = True
                    #   vlines=dict(vlines=datelist, 
                        #colors = colorlist, alpha = .2,linewidths=1),
                    )
        
                        plt.show()
            except:
                print('Error')




    def runTestData(setuptype):

        model = load_model('model_' + setuptype)

        setups = pd.read_feather('C:/Screener/setups/Testdata_' + setuptype + '.feather')
        print(setups)
        #print(setups[setups['setup'] == 1])
        right = 0
        total = 0

        while True:


            try:
                setup = setups.iloc[(random.randint(0,len(setups)-1))]
 

                ticker = setup['ticker'] 
                date =  setup['date']
                typee = setup["setup"]
    
                df = create.test_data(ticker,date)


                sys.stdout = open(os.devnull, 'w')
                god = model.predict(df)

                val = 0
                
                if god[0][1] > god[0][0]:
                    val = 1

                sys.stdout = sys.__stdout__
                #print(f'{val} , {type}')

                if typee == setuptype:
                    actual = 1
                else:
                    actual = 0


                if val == actual:
                    right += 1





                total += 1
                print(f'God 0: {str(god[0][0])} God 1: {str(god[0][1])}')
                print(f"{val} Actual: {typee}")
                if val == 1 or typee == 1:
                    df1 = data.get(ticker)


                    ind= data.findex(df1,date)

                    df1 = df1[ind-100:ind + 1]
                    mc = mpf.make_marketcolors(up='g',down='r')
                    s  = mpf.make_mpf_style(marketcolors=mc)
            
                    mpf.plot(df1, type='candle', volume=True  , 
 
                    style=s, warn_too_much_data=100000,returnfig = True, panel_ratios = (5,1), 
                    tight_layout = True
                #   vlines=dict(vlines=datelist, 
                    #colors = colorlist, alpha = .2,linewidths=1),
                )
                
        
                    plt.show()



                #time.sleep(.1)
            except:
                pass


if __name__ == "__main__":
    setuptype = 'MR'
    Test3.runRandomTicker(setuptype)
    #Test3.runTestData(setuptype)







