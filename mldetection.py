import numpy as np
from typing import Tuple

# NN imports
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Dropout

# Imports for evaluating the network
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Global variables
EPOCHS = 25
BATCH_SIZE = 64
VALIDATION = 0.1
LEARN_RATE = 1e-3
MODEL_SAVE_NAME = 'model'


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
