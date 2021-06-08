from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    transactions = db.relationship('Transaction')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String(1))
    pair = db.Column(db.String(10))
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    fee = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class TempTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    type = db.Column(db.String(1))
    pair = db.Column(db.String(10))
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    fee = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
