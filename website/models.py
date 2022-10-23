from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  name = db.Column(db.String(150))
  cash = db.Column(db.Float)
  remove = db.relationship('Remove')
  entry = db.relationship('Entry')
  custom = db.Column(db.String(150))
  custom1 = db.Column(db.String(150))
  custom2 = db.Column(db.String(150))
  custom3 = db.Column(db.String(150))

class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  category = db.Column(db.String(150))
  difficulty = db.Column(db.Integer)
  cash_add = db.Column(db.Float)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Remove(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  category = db.Column(db.String(150))
  cash_remove = db.Column(db.Float)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
