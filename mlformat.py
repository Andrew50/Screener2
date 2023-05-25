import os
import numpy as np
import pandas as pd
from Data7 import Data
TRAIN_SPLIT = 0.8
FEAT_LENGTH = 50
FEAT_COLS = ['Open', 'Low', 'High', 'Close']
TICKERS = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'GOOG', 'AMD']

def getTickers(): 

    setupsss = pd.read_feather("C:/Screener/setups/EP.feather")
    for iii in range(len(setupsss)):
        Data.get(setupsss.iloc[iii]['ticker'], tf='d', date=setupsss.iloc[iii]['datetime'])

def time_series(df: pd.DataFrame,
                col: str,
                name: str) -> pd.DataFrame:
    '''
    Form the lagged columns for this feature
    '''
    return df.assign(**{
        f'{name}_t-{lag}': col.shift(lag)
        for lag in range(0, FEAT_LENGTH)
    })


def get_lagged_returns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    For each of the feature cols, find the returns and then form the lagged
    time-series as new columns
    '''
    for col in FEAT_COLS:
        print(df[col])
        print(df[col].shift(1))
        return_col = df[col]/df[col].shift(1)-1
        print(return_col)
        print("------------------------------")
        df = time_series(df, return_col, f'feat_{col}_ret')
    return df


def get_classification(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Get the classifications for the LSTM network, which are as follows:
        0 = The 20 period SMA is below the low of the day
        1 = The 20 period SMA is between the low and high of the day
        2 = The 20 period SMA is above the high of the day
    '''
    
    df['ma'] = df['Close'].rolling(20).mean()
    
    conditions = [
        df['ma'] <= df['Low'],
        (df['ma'] < df['High']) & (df['ma'] > df['Low']),
        df['ma'] >= df['High'],
    ]
    
    df['classification'] = np.select(
        condlist = conditions,
        choicelist = [0, 1, 2],
    )
    
    return df
    

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
    
    setup 





    dfs = []
    for ticker in TICKERS:






        df = pd.read_csv(f'data/{ticker}.csv')

        df = get_lagged_returns(df)
        df = get_classification(df)
        
        # We may end up with some divisions by 0 when calculating the returns
        # so to prevent any rows with this slipping in, we replace any infs
        # with nan values and remove all rows with nan values in them
        dfs.append(
            df
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
            [[col for col in df.columns if 'feat_' in col] + ['classification']]
        )
        print(dfs)
    nn_values = pd.concat(dfs).values
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
