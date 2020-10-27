''' Main function for call prediction algorithms'''
import config
import yahoo


map_of_stock_predictions = {}

def main():
    '''Main func'''
    if config.USE_REGRESSION_DAYS:
        result = regression_days()
    else:
        result = stocks_traversal()

    print(result)
    # NOTIFICATION WILL BE DONE VIA API ( PUT HERE )

def stocks_traversal():
    '''
    Traverse through list of stocks to generate predictions
    :return:  predictions data_points
    '''
    for stock in config.STOCK_LIST:
        map_of_stock_predictions[stock] = yahoo.stocks_prediction(config.PREDICTION_DAYS,stock)
    return map_of_stock_predictions

def regression_days():
    '''
    Regression through list of days to generate backward data_points
    :return: return predction per days travesed per stock
    '''
    for prediction_days in config.REGRESSION_OF_DAYS:
        for stock in config.STOCK_LIST:
            map_of_stock_predictions[stock] = yahoo.stocks_prediction(prediction_days,stock)
    return map_of_stock_predictions

if __name__ == '__main__':
    main()
