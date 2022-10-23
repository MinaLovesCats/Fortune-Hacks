from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Entry, Remove
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import matplotlib.pyplot as plt

blueprint = Blueprint('blueprint', __name__)

def make_graph1():
  #x = Entry.id
 # y1 = Entry.cash_add
 # y2 = Entry.difficulty
  x=[1, 2, 3]
  y1=[5, 3, 4]
  y2=[1, 5, 4]
  plt.plot(x, y1, label="Money")
  plt.plot(x, y2, label="Difficulty")
  plt.legend()
  plt.title("Money Per Entry vs Difficulty")
  plt.xlabel("Entry")
  plt.ylabel("Money, Difficulty")
  graph1= plt.savefig("graph1.jpg")

@blueprint.route("/")
def default():
  return render_template("hmm.html")

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password2')
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        login_user(user, remember=True)
        flash('Logged In Sucessfully', category='success')
        return redirect(url_for('blueprint.home'))
      else:
        flash('Incorrect Password', category='error')
    else:
      flash('User doesn\'t exist', category='error')
  return render_template("login.html", user=current_user)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blueprint.login'))
    flash('You Have Been Logged Out.', category='success')

@blueprint.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
      email = request.form.get('email')
      name = request.form.get('name')
      password1 = request.form.get('password1')
      password2 = request.form.get('password2')
      
      user = User.query.filter_by(email=email).all()
      if user:
        flash('Another account uses this email.', category='error')
      elif len(email) < 5:
        flash('Email is too short.', category='error')
      elif len(name) < 2:
        flash('Name is too short.', category='error')
      elif password1 != password2:
        flash('Passwords do not match.', category='error')
      elif len(password1) < 7:
        flash('Password is too short.', category='error')
      else:
        start = 0
        new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'), cash=start)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account Created', category='success')
        return redirect("/home")
        
    return render_template("signup.html", user=current_user)

@blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def home():
  user = current_user
  if not user.custom or not user.custom1 or not user.custom2 or not user.custom3:
    flash("Please go to 'Account' and add all of your custom categories.", category='error')
  if request.method == "POST":
    category = request.form.get('category')
    if category == "custom":
      category = user.custom
    hours = int(request.form.get('hours'))
    minutes = int(request.form.get('minutes'))
    difficulty = request.form.get('difficulty')
    mult = int(difficulty)
    min2= hours*60
    time = minutes + min2
    money = time*mult*0.01
    new_entry = Entry(cash_add = money, category = category, user_id = current_user.id, difficulty = difficulty)
    db.session.add(new_entry)
    db.session.commit()
    oldcash = User.cash
    newcash = oldcash + money
    current_user.cash = newcash
    db.session.commit()
    flash("Entry Submitted.", category="success")
    return redirect("/home")
  return render_template("home.html", user=current_user)

@blueprint.route('/spend', methods=["GET", "POST"])
@login_required
def spend():
  user=current_user
  if request.method == "POST":
    loss = request.form.get('hhh')
    loss = str(loss)
    loss = float(loss)
    current = User.cash
    update = current - loss
    categorr = request.form.get('category')
    if categorr == "custom1":
      category = user.custom1
    elif categorr == "custom2":
      category = user.custom2
    elif categorr == "custom3":
      category = user.custom3
    new_remove = Remove(cash_remove = loss, user_id=current_user.id, category=category)
    db.session.add(new_remove)
    db.session.commit()
    current_user.cash = update
    db.session.commit()
    flash("Money Spent.", category="success")
    return redirect("/home")
  return render_template("spend.html", user=current_user)
  
@blueprint.route('/data', methods=["GET", "POST"])
@login_required
def data():
  if request.method =="POST":
    make_graph1()
  return render_template("data.html", user=current_user)

@blueprint.route('/custom', methods=["GET", "POST"])
@login_required
def custom():
  if request.method == "POST":
    it = request.form.get("custom")
    current_user.custom = it
    db.session.commit()
    it1 = request.form.get("custom1")
    current_user.custom1 = it1
    db.session.commit()
    it2 = request.form.get("custom2")
    current_user.custom2 = it2
    db.session.commit()
    it3 = request.form.get("custom3")
    current_user.custom3 = it3
    db.session.commit()
    flash("Custom category updated!", category="success")
    return redirect("/home")
  return render_template("custom.html", user=current_user)