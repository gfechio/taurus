import yahoo
import notification

stock_list = ["AAPL", "NFLX", "FB", "TSLA", "EBAY", "GOOG", "DOCU", "AMZN", "SNE", "MRNA", "NVDA", "BABA"]
mail_receivers = ["gfechio@gmail.com", "tom.naves@gmail.com"]
#regression_of_days = [20, 15, 10, 7, 5, 2, 1]
prediction_days = 7

#for prediction_days in regression_of_days:
map_of_stock_predictions = {}
for stock in stock_list:
    map_of_stock_predictions[stock] = yahoo.stocks(prediction_days,stock)


#notification.Email.send(to=mail_receivers, title=f"Prediction for {stock_list}  for the next {prediction_days} days.", body=str(map_of_stock_predictions))
