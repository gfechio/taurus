import os

import config
import database

import numpy as np
from datetime import datetime
from smtplib import SMTP
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split

# Yahoo Data
from pandas_datareader import data as pdr
import yfinance as yf

#For Stock Data
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data



def getStocks(n):
    #Navigating to the Yahoo stock screener
    # Testing for Lemonade : <a href="/quote/LMND?p=LMND" title="Lemonade, Inc." class="Fw(600) C($linkColor)" data-reactid="131">LMND</a>
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(config.CHROMEDRIVER, options=options)
    driver.get(config.URL)
    button = driver.find_element_by_name('agree')
    button.click()

    stock_list = []
    n +=1
    #//*[@id="marketsummary-itm-^IXIC"]/h3/a[1]
    #//*[@id="marketsummary-itm-^DJI"]/h3/a[1]
    for i in range(1,n):
        ticker = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[1]/a')
        stock_list.append(ticker.text)

    driver.quit()

    return stock_list

def getIndices(n):
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(config.CHROMEDRIVER, options=options)
    driver.get(config.URL)
    button = driver.find_element_by_name('agree')
    button.click()

    indexes_list = []
    n +=1
    for i in range(1,n):
        ticker = driver.find_element_by_xpath('//*[@id="yfin-list"]/div[2]/div/div/table/tbody/tr['+str(i)+']/td[1]/a')
        indexes_list.append(ticker.text)

    driver.quit()

    return indexes_list
