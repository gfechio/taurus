'''LSTM model to process data and create predictions '''
import math
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

plt.style.use('fivethirtyeight')

def generate_model(data_reader):
    '''
    :param data_reader: panda formatted data
    :return: model and data defined for prediction
    '''
    #Create a new dataframe with only the 'Close' column
    data = data_reader.filter(['Close'])
    #Converting the dataframe to a numpy array
    dataset = data.values
    #Get /Compute the number of rows to train the model on
    training_data_len = math.ceil( len(dataset) *.8)

    #Scale the all of the data to be values between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    #Create the scaled training data set
    train_data = scaled_data[0:training_data_len  , : ]
    #Split the data into x_train and y_train data sets
    x_train=[]
    y_train = []
    for i in range(60,len(train_data)):
        x_train.append(train_data[i-60:i,0])
        y_train.append(train_data[i,0])

    #Convert x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    #Reshape the data into the shape accepted by the LSTM
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

    #Build the LSTM network model
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
    model.add(keras.layers.LSTM(units=50, return_sequences=False))
    model.add(keras.layers.Dense(units=25))
    model.add(keras.layers.Dense(units=1))

    #Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    #Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    #Test data set
    test_data = scaled_data[training_data_len - 60: , : ]
    #Create the x_test and y_test data sets
    x_test = []
    #Get all of the rows from index 1603 to the rest and all of the columns
    # (in this case it's only column 'Close'), so 2003 - 1603 = 400 rows of data
    y_test =  dataset[training_data_len : , : ]

    return y_test, x_test, model, scaler, test_data

def predict(y_test, x_test, model, scaler, test_data):
    '''
    Prediction model
    :param y_test: Y_test
    :param x_test: X_test
    :param model: model
    :param scaler: scaler
    :param test_data: data
    :return:
    '''
    for i in range(60,len(test_data)):
        x_test.append(test_data[i-60:i,0])

    #Convert x_test to a numpy array
    x_test = np.array(x_test)

    #Reshape the data into the shape accepted by the LSTM
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

    #Getting the models predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)#Undo scaling

    return predictions

def root_deviation(predictions, y_test):
    '''
    Calculate/Get the value of RMSE
    :param predictions: data from predictions
    :param y_test: y value to generate deviation
    :return: Deviation data_points
    '''
    return [ np.sqrt(np.mean(((predictions- y_test)**2))) ]
