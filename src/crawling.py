import os

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


CHROMEDRIVER = "/usr/local/sbin/chromedriver"
EXPORT_DIR = "/home/gfechio/Trading/Exports"
URL = "https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202"

def getStocks(n):
    #Navigating to the Yahoo stock screener
    # Testing for Lemonade : <a href="/quote/LMND?p=LMND" title="Lemonade, Inc." class="Fw(600) C($linkColor)" data-reactid="131">LMND</a>
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
    driver.get(URL)
    button = driver.find_element_by_name('agree')
    button.click()

    stock_list = []
    n +=1
    for i in range(1,n):
        ticker = driver.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[1]/a')
        stock_list.append(ticker.text)

    driver.quit()

    return stock_list

def predictData(stock, days):
    start = datetime(2019, 1, 1)
    end = datetime.now()
    #Outputting the Historical data into a .csv for later use
    #df = get_historical_data(stock, start=start, end=end, output_format='pandas')
    yf.pdr_override()
    df = pdr.get_data_yahoo(stock, start=start, end=end)

    db = database.Database("historical")
    db.panda_write(df)
    

    if not os.path.exists(EXPORT_DIR):
        os.mkdir(EXPORT_DIR)

    csv_name = (EXPORT_DIR+'/' + stock + '_Export.csv')
    df.to_csv(csv_name)
    df['prediction'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    forecast_time = int(days)


    X = np.array(df.drop(['prediction'], 1))
    Y = np.array(df['prediction'])
    X = preprocessing.scale(X)
    X_prediction = X[-forecast_time:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5)
    #a_train, a_test, b_train, b_test = train_test_split(a, b, 
    #                                     test_size=0.33, random_state=42)

    #Performing the Regression on the training data
    clf = LinearRegression()
    clf.fit(X_train, Y_train)
    prediction = (clf.predict(X_prediction))
    print(prediction)

    last_row = df.tail(1)
    if (float(prediction[4]) > (float(last_row['Close']))):
        output = ("\n\nStock:" + str(stock) + "\nPrior Close:\n" +         str(last_row['Close']) + "\n\nPrediction in 1 Day: " + str(prediction[0]) + "\nPrediction in 5 Days: " + str(prediction[4]))
    else:
        output = ("\n\nOUT OF PREDITCION -- Stock:" + str(stock) + "\nPrior Close:\n" +         str(last_row['Close']) + "\n\nPrediction in 1 Day: " + str(prediction[0]) + "\nPrediction in 5 Days: " + str(prediction[4]))

def send_message(output):
    email = "gfechio@gmail.com"

    msg = f"From: {email} To: {email} {output}"
    with SMTP("localhost") as smtp:
        smtp.sendmail("gfechio@carnage", email, msg)


if __name__ == '__main__':
    stock_list = getStocks(10)
    output_content = []
    for stock in stock_list:
        try:
            output_content.append(predictData(stock, 1))
        except:
            output_content.append(f"Stock: {stock} was not predicted")
    
    print(output_content)
    send_message(str(output_content))
    


