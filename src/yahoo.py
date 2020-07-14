import time

import config
import database
import prediction
import yscrapper

import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr


def stocks(prediction_days, stock):
    print(f"Executing prediction for {stock}")
    yf.pdr_override()
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()+86400))
    data = pdr.get_data_yahoo(stock, start=config.HISTORY_START_DATE, end=now)
    db = database.Database()
    db.use("taurus")
    db.panda_write("taurus", data, stock)

    prediction_results = prediction.simple_prediction(stock, prediction_days, data)

    result = {}
    day_time = time.time()
    for single_prediction in prediction_results:
        day_time = day_time +  86400 # Seconds in a day
        date = time.strftime('%Y-%m-%d', time.localtime(day_time))
        result[date] = single_prediction

    df = pd.DataFrame(list(result.items()), columns = ['Date', 'Prediction'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.set_index(df['Date'])
    df = df = df.drop(['Date'], axis=1)
    db.panda_write("taurus", df, stock)
    df.to_csv(header=None, index=False).strip('\n').split('\n')

    return df

def indices(prediction_days, index):
    print(f"Executing prediction for {index}")
    yf.pdr_override()
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()+86400))
    data = pdr.get_data_yahoo(index, start=config.HISTORY_START_DATE, end=now)
    db = database.Database()
    db.use("taurus")
    db.panda_write("taurus", data, index)

    prediction_results = prediction.simple_prediction(index, prediction_days, data)

    result = {}
    day_time = time.time()
    for single_prediction in prediction_results:
        day_time = day_time +  86400 # Seconds in a day
        date = time.strftime('%Y-%m-%d', time.localtime(day_time))
        result[date] = single_prediction

    df = pd.DataFrame(list(result.items()), columns = ['Date', 'Prediction'])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.set_index(df['Date'])
    df = df = df.drop(['Date'], axis=1)

    db.panda_write("taurus", df, index)
    df.to_csv(header=None, index=False).strip('\n').split('\n')

    return True


# get stock info
#print(stock.info)
## get historical market data
#hist = stock.history(period="max")
#print(hist)
#
## show actions (dividends, splits)
#print(stock.actions)
#
## show dividends
#stock.dividends
#
## show splits
#stock.splits
#
## show financials
#stock.financials
#stock.quarterly_financials
#
## show major holders
#stock.major_holders
#
## show institutional holders
#stock.institutional_holders
#
## show balance heet
#stock.balance_sheet
#stock.quarterly_balance_sheet
#
## show cashflow
#stock.cashflow
#stock.quarterly_cashflow
#
## show earnings
#stock.earnings
#stock.quarterly_earnings
#
## show sustainability
#stock.sustainability

# show analysts recommendations
#print(stock.recommendations)

## show next event (earnings, etc)
#stock.calendar
#
## show ISIN code - *experimental*
## ISIN = International Securities Identification Number
#stock.isin
#
## show options expirations
#stock.options

# get option chain for specific expiration
#opt = stock.option_chain('2020-07-31')
# data available via: opt.calls, opt.puts