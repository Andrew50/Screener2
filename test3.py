

import random
import pandas as pd
from Create import Create as create
import time
import sys, os
from tensorflow.keras.models import load_model
import mplfinance as mpf
from Data7 import Data as data
model = load_model('model')


setups = pd.read_feather('C:/Screener/setups/Testdata.feather')
print(setups[setups['setup'] == 1])
right = 0
total = 0
from matplotlib import pyplot as plt
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

        if typee == 'EP':
            actual = 1
        else:
            actual = 0


        if val == actual:
            right += 1





        total += 1
        print(val)
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



        #time.sleep(.1)
    except TimeoutError:
        pass











