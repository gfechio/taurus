from datetime import datetime 
from flask import flash, redirect, render_template, url_for
from flask import Flask, request, jsonify
from flask_restx import Api, Namespace, Resource, fields

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

from todo import api as todo
from stocks import api as stocks

api.add_namespace(todo)
api.add_namespace(stocks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)