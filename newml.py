import os
import numpy as np
import pandas as pd
from Data7 import Data as data
TRAIN_SPLIT = 0.8
FEAT_LENGTH = 30
FEAT_COLS = ['open', 'low', 'high', 'close']
#FEAT_COLS = ['Open', 'Low', 'High', 'Close']
TICKERS = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'GOOG', 'AMD']

def getTickers(): 

    setupsss = pd.read_feather("C:/Screener/setups/EP.feather")
    for iii in range(len(setupsss)):
        Data.get(setupsss.iloc[iii]['ticker'], tf='d', date=setupsss.iloc[iii]['datetime'])



def get_lagged_returns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    For each of the feature cols, find the returns and then form the lagged
    time-series as new columns
    '''
    add = []
    for row in range(len(df)):
        if(row != 0):
            add.append((df.iloc[row]['open']/df.iloc[row-1]['close'])-1)
            add.append((df.iloc[row]['high']/df.iloc[row-1]['close'])-1)
            add.append((df.iloc[row]['low']/df.iloc[row-1]['close'])-1)
            add.append((df.iloc[row]['close']/df.iloc[row-1]['close'])-1)
    return add



def reshape_x(x: np.array) -> np.array:
    '''
    If an RNN-type network is wanted, reshape the input so that it is a 3D
    array of the form (sample, time series, feature).
    
    Parameters
    ----------
    x : np.arr
    Returns
    -------
    x_reshaped : np_arr
        The reshaped x array for the LSTM
    '''
    
    # Calculate the number of features we have in the nn (assumes all features
    # are of the same length)
    num_feats = x.shape[1]//FEAT_LENGTH
    
    # Initialise the new x array with the correct size
    x_reshaped = np.zeros((x.shape[0], FEAT_LENGTH, num_feats))
    
    # Populate this array through iteration
    for n in range(0, num_feats):
        x_reshaped[:, :, n] = x[:, n*FEAT_LENGTH:(n+1)*FEAT_LENGTH]
    
    return x_reshaped


def get_nn_data():
    '''
    For all tickers, deduce the NN features and classifications, and then save
    the outputs as four numpy arrays (x_train, y_train, x_test, y_test)
    '''
    setup = 'EP'
    setups = pd.read_feather('C:/Screener/setups/' + setup + '.feather')






    dfs = []
    #for ticker in TICKERS:
    print(setups)
    for i in range(len(setups)):

        ticker = setups.iat[i,0]
        date = setups.iat[i,1]
        value = setups.iat[i,2]
        if(ticker != "RCII"):
            try:
                print(ticker)
                df = data.get(str(ticker))
            except:
                print(f'{ticker} fucked')
       
            index = data.findex(df,date)
            if(index != None): 
                df2 = df[index-51:index]

                o = df.iat[index,0]
                add = pd.DataFrame({
                    'datetime':[date],
                    'open':[o],
                    'high':[o],
                    'low':[o],
                    'close':[o],
                    'volume':[0]}).set_index('datetime')
                df2 = pd.concat([df2,add])
                df = df2
               # print(df)
                #df = pd.read_csv(f'data/{ticker}.csv')
                added = get_lagged_returns(df)
                added.append(value)
                #print(df)
                #print(added)
                # We may end up with some divisions by 0 when calculating the returns
                # so to prevent any rows with this slipping in, we replace any infs
                # with nan values and remove all rows with nan values in them
                addeddf = pd.DataFrame([added])
                #print(addeddf)
                dfs.append(addeddf)
        
    nn_values = pd.concat(dfs).reset_index(drop = True)
    nn_values = nn_values.dropna()
    nn_values = nn_values.reset_index(drop = True)
    nn_values = nn_values.rename({204: "classification"}, axis=1)
    print(nn_values)
    nn_values.to_csv('C:/Screener/godddd.csv')
   
    nn_values = nn_values.values
    #print(dfs)
    # Shuffle the values to ensure the NN does not learn an order
    np.random.shuffle(nn_values)


    
    # Split into training and test data
    split_idx = int(TRAIN_SPLIT*nn_values.shape[0])
    
    # Save the x training data
    np.save('x_train', reshape_x(nn_values[0:split_idx, :-1]))
    
    # Save the y training data
    np.save('y_train', nn_values[0:split_idx:, -1])
    
    # Save the x testing data
    np.save('x_test', reshape_x(nn_values[split_idx:, :-1]))
    
    # Save the y testing data
    np.save('y_test', nn_values[split_idx:, -1])
    
    return
    

if __name__ == '__main__':
    
    get_nn_data()

