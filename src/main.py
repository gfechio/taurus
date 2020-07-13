import yahoo
import notification

stock_list = ["EBAY", "GOOG", "DOCU", "TMHC", "AMZN", "SNE"]
mail_receivers = ["gfechio@gmail.com", "tom.naves@gmail.com"]
prediction_days = 7

map_of_stock_predictions = {}
for stock in stock_list:
    map_of_stock_predictions[stock] = yahoo.stocks(prediction_days,stock)

notification.Email.send(to=mail_receivers, title=f"Prediction for {stock_list}  for the next {prediction_days} days.", body=str(map_of_stock_predictions))
