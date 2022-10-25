from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(150), nullable=False)
  name = db.Column(db.String(150), nullable=False)
  cash = db.Column(db.Numeric(15, 2))
  theme = db.Column(db.Integer)
  date = db.Column(db.DateTime(), default=datetime.now())
  remove = db.relationship('Remove')
  entry = db.relationship('Entry')
  entrycat = db.relationship('Entrycat')
  customtype2 = db.relationship('CustomType2')
  big = db.relationship('Big')
  minigoal = db.relationship('MiniGoal')
  customtype5 = db.relationship('CustomType5')

class Entry(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  difficulty = db.Column(db.Integer)
  hours = db.Column(db.Integer)
  minutes = db.Column(db.Integer)
  cash_add = db.Column(db.Numeric(15, 2))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category = db.Column(db.String)
  categoryid = db.Column(db.Integer, db.ForeignKey('entrycat.id'))

class Remove(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  cash_remove = db.Column(db.Numeric(15, 2))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category = db.Column(db.String)
  categoryid = db.Column(db.Integer, db.ForeignKey('entrycat.id'))

class Entrycat(db.Model): #categories of productive things to enter
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  type = db.Column(db.String(150))
  entry = db.relationship('Entry')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CustomType2(db.Model): #categories of spending
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  type = db.Column(db.String(150))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Big(db.Model): #overarching goals
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  biggoal = db.Column(db.String(150))
  thours = db.Column(db.Integer)
  chours = db.Column(db.Integer) #remember: set to 0 when making new goal
  deadline = db.Column(db.Date())
  bigreward = db.Column(db.Numeric(15, 2))
  minigoal = db.relationship('MiniGoal')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class MiniGoal(db.Model): #sub goals
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  goal = db.Column(db.String(150))
  deadline = db.Column(db.Date())
  thours = db.Column(db.Integer)
  tmins = db.Column(db.Integer)
  chours = db.Column(db.Integer)
  tmins = db.Column(db.Integer)
  reward = db.Column(db.Numeric(15, 2))
  customtype3_id = db.Column(db.Integer, db.ForeignKey('big.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CustomType5(db.Model): #stand alone goals
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.now())
  reward = db.Column(db.Numeric(15, 2))
  deadline = db.Column(db.Date())
  thours = db.Column(db.Integer)
  tmins = db.Column(db.Integer)
  chours = db.Column(db.Integer)
  tmins = db.Column(db.Integer)
  goal = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))