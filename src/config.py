
#Main
STOCK_LIST = ["AAPL", "NFLX", "FB", "TSLA", "EBAY", "GOOG", "DOCU", "AMZN", "SNE", "MRNA", "NVDA", "BABA"]
REGRESSION_OF_DAYS = [20, 15, 10, 7, 5, 2, 1]
PREDICTION_DAYS = 7
USE_REGRESSION_DAYS = False

# Yahoo
HISTORY_START_DATE = "2019-01-01" 

# Scrapper
CHROMEDRIVER = "/usr/local/sbin/chromedriver"
URL = "https://in.finance.yahoo.com/world-indices"

# Notification
MAIL_RECEIVERS = ["gfechio@gmail.com", "tom.naves@gmail.com"]
MAIL_FROM = "taurus@localhost"
# Prediction

# DataBase
DB_HOST = "localhost"
DB_PORT = 8086
DB_NAME = "taurus"