'''API to deal wiht Stacks configuration '''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Namespace, Resource

import sqlalchemy.orm

stocks = Flask(__name__)
stocks.config.from_pyfile('api.cfg')
db = SQLAlchemy(stocks)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
api = Namespace('api/stocks', description='Taurus Stocks Operations.')

@api.route('/stocks')
@api.doc('Manage Stocks list to check.')
@api.param('stock', 'AAPL', location='arg')
class Stocks(Resource):
    '''
    Stock management service
    '''
    def get(self):
        '''
        Get stocks that are being predicted
        :return:
        '''
        stock_param = request.args.get('stocks')
        if stock_param is None:
            msg = 'The "stock" parameter is required.'
            api.abort(400, msg)

        return jsonify("stock list with configuration")
