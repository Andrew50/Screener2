
import os
import numpy as np
import pandas as pd
from Data7 import Data as data

import numpy as np
from typing import Tuple

# NN imports
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Dropout

# Imports for evaluating the network
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Global variables
EPOCHS = 5
BATCH_SIZE = 64
VALIDATION = 0.1
LEARN_RATE = 1e-3
MODEL_SAVE_NAME = 'model'
TRAIN_SPLIT = 0.8
FEAT_LENGTH = 50
FEAT_COLS = ['open', 'low', 'high', 'close']
#FEAT_COLS = ['Open', 'Low', 'High', 'Close']
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
        #print(df[col])
        #print(df[col].shift(1))
        return_col = df[col]/df[col].shift(1)-1
       # print(return_col)
     #   print("------------------------------")
        
        df = time_series(df, return_col, f'feat_{col}_ret')
    #df.to_csv('C:/Screener/godddd.csv')
    return df


def get_classification(df: pd.DataFrame,value) -> pd.DataFrame:
    '''
    Get the classifications for the LSTM network, which are as follows:
        0 = The 20 period SMA is below the low of the day
        1 = The 20 period SMA is between the low and high of the day
        2 = The 20 period SMA is above the high of the day
    '''
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
    '''
    df['classification'] = value
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
    setup = 'EP'
    setups = pd.read_feather('C:/Screener/setups/' + setup + '.feather')






    dfs = []
    #for ticker in TICKERS:
    for i in range(len(setups)):
        ticker = setups.iat[i,0]
        date = setups.iat[i,1]
        value = setups.iat[i,2]

        df = data.get(ticker)

       
        index = data.findex(df,date)
        df2 = df[index-50:index]

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


        #df = pd.read_csv(f'data/{ticker}.csv')
        df = get_lagged_returns(df)
      #  print(df)
        df = get_classification(df,value)
     #   print(df)
        
        # We may end up with some divisions by 0 when calculating the returns
        # so to prevent any rows with this slipping in, we replace any infs
        # with nan values and remove all rows with nan values in them
        dfs.append(
            df
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
            [[col for col in df.columns if 'feat_' in col] + ['classification']]
        )
        
    nn_values = pd.concat(dfs)
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
   
def load_data() -> Tuple[np.array, np.array, np.array, np.array]:
    '''
    Load in the pre-processed price data ready for the LSTM
    '''
    return (
        np.load('x_train.npy'),
        np.load('y_train.npy'),
        np.load('x_test.npy'),
        np.load('y_test.npy'),
    )


def get_model(x_train: np.array) -> Sequential:
    '''
    Generate the NN model that we are going to train
    '''
    return Sequential([
        Bidirectional(
            LSTM(
                64, 
                input_shape = (x_train.shape[1], x_train.shape[2]),
                return_sequences = True,
            ),
        ),
        Dropout(0.2),
        Bidirectional(LSTM(32)),
        Dense(3, activation = 'softmax'),
    ])


def evaluate_training(model: Sequential,
                      x_test: np.array,
                      y_test: np.array):
    '''
    Produce confusion matrices to evaluate the training on the testing data.
    '''
    
    score = model.evaluate(
        x_test,
        y_test,
        verbose = 0,
    )

    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
    
    pred = np.argmax(
        model.predict(x_test), 
        axis = 1,
    )
    
    cm = confusion_matrix(
        y_true = y_test,
        y_pred = pred,
    )
    
    # The scaled confusion matrix gives a view where each column is scaled
    # by the total sum of elements in that column
    cm_scaled = cm/cm.astype(np.float).sum(axis = 0)
    
    unscaled = ConfusionMatrixDisplay(confusion_matrix = cm)
    unscaled.plot()
    unscaled.ax_.set_title('Unscaled confusion matrix')
    
    scaled = ConfusionMatrixDisplay(confusion_matrix = cm_scaled)
    scaled.plot()
    scaled.ax_.set_title('Scaled confusion matrix')
    
    return


if __name__ == '__main__':
    
    get_nn_data()
    x_train, y_train, x_test, y_test = load_data()
    
    model = get_model(x_train)
    
    model.compile(
        loss = 'sparse_categorical_crossentropy',
        optimizer = Adam(learning_rate = LEARN_RATE),
        metrics = ['accuracy']
    )
    
    model.fit(
        x_train,
        y_train,
        epochs = EPOCHS,
        batch_size = BATCH_SIZE,
        validation_split = VALIDATION,
    )
    
    evaluate_training(model, x_test, y_test)
    
    model.save(MODEL_SAVE_NAME)