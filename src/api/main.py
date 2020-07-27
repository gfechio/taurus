from datetime import datetime 
from flask import flash, redirect, render_template, url_for
from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace, Resource, fields

import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

app = Flask(__name__)
app.config.from_pyfile('api.cfg')
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
api = Api(
    app,
    base_url='/api/',
    base_path='/api/',
    doc='/api/',
    version='0.1',
    title='Taurus',
    description='Taurus API.'
)

ns = api.namespace('/api', description='Taurus Operations.')

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column("todo_id", db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()



@ns.route('/todo/')
class Todo(Resource):
    def get():
        return render_template(
            "show_all.html", todos=Todo.query.order_by(Todo.pub_date.desc()).all()
        )
    def post():
        if not request.form["title"]:
            flash("Title is required", "error")
        elif not request.form["text"]:
            flash("Text is required", "error")
        else:
            todo = Todo(request.form["title"], request.form["text"])
            db.session.add(todo)
            db.session.commit()
            flash("Todo item was successfully created")
            return redirect(url_for("show_all"))

        return render_template("new.html")

    def put():
        for todo in Todo.query.all():
            todo.done = f"done.{todo.id}" in request.form
        flash("Updated status")
        db.session.commit()
        return redirect(url_for("show_all"))

@ns.route('/stocks')
@ns.doc('Manage Stocks list to check.')
@ns.param('stock', 'AAPL', location='arg')
class Stocks(Resource):
    def get(self):
        stocks = request.args.get('stocks')
        if stocks is None:
            msg = 'The "stock" parameter is required.'
            api.abort(400, msg)

        return jsonify(stocks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)