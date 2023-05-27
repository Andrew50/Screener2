

import random
import pandas as pd
from Create import Create as create
import time
import sys, os
from tensorflow.keras.models import load_model
model = load_model('model')


setups = pd.read_feather('C:/Screener/sync/setups.feather')


while True:
    try:
        setup = setups.iloc[(random.randint(0,len(setups)-1))]
 

        ticker = setup['Ticker'] 
        date =  setup['Date']
    
        df = create.test_data(ticker,date)


        sys.stdout = open(os.devnull, 'w')
        god = model.predict(df)

        val = 0
        if god[0][1] > god[0][0]:
            val = 1

        sys.stdout = sys.__stdout__
        print(f'{val} , {setup["Setup"]}')
   
        time.sleep(.1)
    except:
        pass











