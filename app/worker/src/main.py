import config
import yahoo


map_of_stock_predictions = {}

def main():
    if config.USE_REGRESSION_DAYS:
        result = regression_days()
    else:
        result = stocks_traversal()

    # NOTIFICATION WILL BE DONE VIA API ( PUT HERE ) 

def stocks_traversal():
    for stock in config.STOCK_LIST:
        map_of_stock_predictions[stock] = yahoo.stocks_prediction(config.PREDICTION_DAYS,stock)
    return map_of_stock_predictions

def regression_days():
    for prediction_days in config.REGRESSION_OF_DAYS:
        for stock in config.STOCK_LIST:
            map_of_stock_predictions[stock] = yahoo.stocks_prediction(config.PREDICTION_DAYS,stock)
    return map_of_stock_predictions

if __name__ == '__main__':
    main()
