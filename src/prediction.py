import os

import time
import numpy as np
from datetime import datetime

import scipy.stats as si
import sympy as sy
from sympy.stats import Normal, cdf
from sympy import init_printing

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

    #Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))

    return prediction


def black_scholes(S, K, days, r, sigma, option = 'call'): 
    #(stock, days, data_reader)
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option == 'call':
        result = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    if option == 'put':
        result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
        
    return result

def sym_black_scholes(S, K, T, r, sigma, option = 'call'):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    N = Normal('x', 0.0, 1.0)
    
    d1 = (sy.ln(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
    d2 = (sy.ln(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
    
    if option == 'call':
        result = (S * cdf(N)(d1) - K * sy.exp(-r * T) * cdf(N)(d2))
    if option == 'put':
        result = (K * sy.exp(-r * T) * cdf(N)(-d2) - S * cdf(N)(-d1))
        
    return result

def black_scholes_dividend(S, K, T, r, q, sigma, option = 'call'):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #q: rate of continuous dividend paying asset 
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option == 'call':
        result = (S * np.exp(-q * T) * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    if option == 'put':
        result = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * np.exp(-q * T) * si.norm.cdf(-d1, 0.0, 1.0))
        
    return result

def sym_black_scholes_dividend(S, K, T, r, q, sigma, option = 'call'):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #q: rate of continuous dividend paying asset 
    #sigma: volatility of underlying asset
    
    N = Normal('x', 0.0, 1.0)
    
    d1 = (sy.ln(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
    d2 = (sy.ln(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * sy.sqrt(T))
    
    if option == 'call':
        result = S * sy.exp(-q * T) * cdf(N)(d1) - K * sy.exp(-r * T) * cdf(N)(d2)
    if option == 'put':
        result = K * sy.exp(-r * T) * cdf(N)(-d2) - S * sy.exp(-q * T) * cdf(N)(-d1)
        
    return result

