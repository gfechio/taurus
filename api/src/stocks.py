from datetime import datetime 
from flask import flash, redirect, render_template, url_for
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace, Resource, fields

import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

stocks = Flask(__name__)
stocks.config.from_pyfile('api.cfg')
db = SQLAlchemy(stocks)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
api = Namespace('api/stocks', description='Taurus Stocks Operations.')

@api.route('/stocks')
@api.doc('Manage Stocks list to check.')
@api.param('stock', 'AAPL', location='arg')
class Stocks(Resource):
    def get(self):
        stocks = request.args.get('stocks')
        if stocks is None:
            msg = 'The "stock" parameter is required.'
            api.abort(400, msg)

        return jsonify(stocks)