

import random
import pandas as pd
from Create import Create as create
import time
import sys, os
from tensorflow.keras.models import load_model
model = load_model('model')


setups = pd.read_feather('C:/Screener/setups/Testdata.feather')
print(setups[setups['setup'] == 1])
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
        print(f'{val} , {typee}')

        if typee == 'EP':
            actual = 1
        else:
            actual = 0


        if val == actual:
            right += 1


        total += 1


        print((right/total) * 100)
        #time.sleep(.1)
    except TimeoutError:
        pass











