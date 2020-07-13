import yfinance as yf
from pandas_datareader import data as pdr

import database

stock_name = "EBAY"
yf.pdr_override()
stock = yf.Ticker(stock_name)
data = pdr.get_data_yahoo(stock_name, start="2019-01-01", end="2020-07-13")
db = database.Database("historical")
db.use()
db.panda_write(data, stock_name)

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