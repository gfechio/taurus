import config
import yahoo
import notification


map_of_stock_predictions = {}

def main():
    if config.USE_REGRESSION_DAYS:
        result = regression_days()
    else:
        result = stocks_traversal()

    #notification.Email.send(title=f"Prediction for {config.STOCK_LIST}  for the next {config.PREDICTION_DAYS} days.", body=str(result))

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
