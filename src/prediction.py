import os

import numpy as np
from datetime import datetime
import time

#For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split

def simple_prediction(stock, days, data_reader):
    data_reader['prediction'] = data_reader['Close'].shift(-1)
    data_reader.dropna(inplace=True)
    forecast_time = int(days)

    X = np.array(data_reader.drop(['prediction'], 1))
    Y = np.array(data_reader['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5)
    #a_train, a_test, b_train, b_test = train_test_split(a, b, 
    #                                     test_size=0.33, random_state=42)

    #Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    return prediction

