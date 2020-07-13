import yfinance as yf
import pandas as pd
import time

from pandas_datareader import data as pdr

import database
import prediction

def stocks(prediction_days, stock):
    print(f"Executing prediction for {stock}")
    yf.pdr_override()
    data = pdr.get_data_yahoo(stock, start="2019-07-10", end="2020-07-13")
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

def indices(prediction_day, index):
    return True

# get stock info
#print(stock.info)
#
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