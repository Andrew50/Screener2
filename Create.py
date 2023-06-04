
import os
import numpy as np
import pandas as pd
from Data7 import Data as data

import numpy as np
from typing import Tuple
from tqdm import tqdm
from matplotlib import pyplot as plt

# NN imports
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Dropout

# Imports for evaluating the network
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

EPOCHS = 10
BATCH_SIZE = 64
VALIDATION = 0.1
LEARN_RATE = 1e-3
MODEL_SAVE_NAME = 'model'
TRAIN_SPLIT = 0.8
FEAT_LENGTH = 50
FEAT_COLS = ['open', 'low', 'high', 'close']
#FEAT_COLS = ['Open', 'Low', 'High', 'Close']
TICKERS = ['TSLA', 'AAPL', 'MSFT', 'NVDA', 'GOOG', 'AMD']

class Create:




# Global variables
    


    def time_series(df: pd.DataFrame,
                    col: str,
                    name: str) -> pd.DataFrame:

        return df.assign(**{
            f'{name}_t-{lag}': col.shift(lag)
            for lag in range(0, FEAT_LENGTH)
        })


    def get_lagged_returns(df: pd.DataFrame) -> pd.DataFrame:

        close = df.iat[-2,3]
        for col in FEAT_COLS:

            return_col = df[col]/df[col].shift(1)-1
            
            
            #df = Create.time_series(df, return_col, f'feat_{col}_ret')


            #return_col = df[col].div(close) - 1

            df = Create.time_series(df, return_col, f'feat_{col}_ret')
            
        return df


    def get_classification(df: pd.DataFrame,value) -> pd.DataFrame:
    
        df['classification'] = value
        return df
    

    def reshape_x(x: np.array) -> np.array:
    
        num_feats = x.shape[1]//FEAT_LENGTH
    
        # Initialise the new x array with the correct size
        x_reshaped = np.zeros((x.shape[0], FEAT_LENGTH, num_feats))
    
        # Populate this array through iteration
        for n in range(0, num_feats):
            x_reshaped[:, :, n] = x[:, n*FEAT_LENGTH:(n+1)*FEAT_LENGTH]
    
        return x_reshaped

    def nn_multi(bar):
        try:

            setups = bar
            

            ticker = setups[0]
            date = setups[1]
            value = setups[2]
            setup_type = [3]

            df = data.get(ticker)


            if 'EP' in setup_type:
                sample_size = 5
            elif setup_type == 'MR':
                sample_size = 15
            elif 'F' in setup_type:
                sample_size = 40
            else:
                sample_size = 10



       
            index = data.findex(df,date)
            df2 = df[index-sample_size:index]

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
            df = Create.get_lagged_returns(df)
            print(df.tail())
            df = Create.get_classification(df,value)
        
            # We may end up with some divisions by 0 when calculating the returns
            # so to prevent any rows with this slipping in, we replace any infs
            # with nan values and remove all rows with nan values in them
            #print(df.replace([np.inf, -np.inf], np.nan).dropna()[[col for col in df.columns if 'feat_' in col] + ['classification']])

            return df.replace([np.inf, -np.inf], np.nan).dropna()[[col for col in df.columns if 'feat_' in col] + ['classification']]
            
        except TimeoutError:
            pass




    def get_nn_data(setuptype,use,split):
 
        setup = setuptype
        allsetups = pd.read_feather('C:/Screener/setups/database/' + setup + '.feather')
        
        
        
        yes = allsetups[allsetups['setup'] == 1]
        no = allsetups[allsetups['setup'] == 0]
        

        length = (len(yes) / use) - len(yes)

        use = length / len(no)


        no = no.sample(frac = use)


        allsetups = pd.concat([yes,no]).sample(frac = 1).reset_index(drop = True)


        if split:
            eighty = int(len(allsetups) * 0.8)
            setups = allsetups.loc[0:eighty].reset_index(drop = True)
            rest = allsetups.loc[eighty:].reset_index(drop = True)
            rest.to_feather('C:/Screener/setups/database/Testdata_' + setup + '.feather')
            TRAIN_SPLIT = 0.8
        else:
            setups = allsetups
            TRAIN_SPLIT = 1
        
            
       # print(setups)
        print(f"Setup Ratio: {len(setups[setups['setup'] == 1]) / len(setups)}")
        

        arglist = []
        for i in range(len(setups)):
            bar = setups.iloc[i].tolist()#.append(setuptype)
           # print(bar)
            arglist.append(bar)

        dfs = data.pool(Create.nn_multi,arglist)

        nn_values = pd.concat(dfs)
       
        nn_values = nn_values.values

    
        #print(dfs)
        # Shuffle the values to ensure the NN does not learn an order
        np.random.shuffle(nn_values)


    
        # Split into training and test data
        if TRAIN_SPLIT == 1:
            split_idx = -1
        else:
            split_idx = int(TRAIN_SPLIT*nn_values.shape[0])
            # Save the x testing data
            np.save('x_test', Create.reshape_x(nn_values[split_idx:, :-1]))
            # Save the y testing data
            np.save('y_test', nn_values[split_idx:, -1])
    
        # Save the x training data
        np.save('x_train', Create.reshape_x(nn_values[0:split_idx, :-1]))
    
        # Save the y training data
        np.save('y_train', nn_values[0:split_idx:, -1])


            
    
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




    def test_data(ticker,date):


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
        df = Create.get_lagged_returns(df)
        #  print(df)
        df = Create.get_classification(df,1)

        df = (
        df
        .dropna()
        .reset_index(drop = True)
        )
    
        x = Create.reshape_x(
            df[[col for col in df.columns if 'feat_' in col] + ['classification']]
            .values[:, :-1]
        )

        return x







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
        
        plt.show()

        return





    def run(setuptype,keep,split):
        
        Create.get_nn_data(setuptype,keep,split)
        x_train, y_train, x_test, y_test = Create.load_data()
    
        model = Create.get_model(x_train)
    
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
    

        if split:
            Create.evaluate_training(model, x_test, y_test)
    
        model.save('C:/Screener/setups/models/model_' + setuptype)

        print('done with model')

if __name__ == '__main__':
    setuptype = 'EP'
    keep = .14
    Create.run(setuptype,keep,False)
    



    
    