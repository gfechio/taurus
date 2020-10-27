'''Start Flask API'''
from flask import Flask
from flask_restx import Api

from stocks import api as stocks

app = Flask(__name__)
api = Api(
    app,
    base_url='/api/',
    base_path='/api/',
    doc='/api/',
    version='0.1',
    title='Taurus',
    description='Taurus API.'
)

ns = api.namespace('', description='Taurus Operations.')
api.add_namespace(stocks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
