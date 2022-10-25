from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Entry, Remove, Entrycat, CustomType2, Big, MiniGoal, CustomType5
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

blueprint = Blueprint('blueprint', __name__)

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
            start = 5.00
            new_user = User(email=email,
                            name=name,
                            password=generate_password_hash(password1,
                                                            method='sha256'),
                            cash=start)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created', category='success')
            flash('Please go to the dropdown menu "Account". Use "Custom Activity Categories" and "Custom Spending Categories" to make a few categories.', category='error')
            return redirect("/home")
    return render_template("signup.html", user=current_user)


@blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user = current_user
    if request.method == "POST":
        categoryid = request.form.get('category')
        cat = Entrycat.query.filter_by(id=categoryid).all()
        for entrycat in cat:
          category = entrycat.type
        hours = int(request.form.get('hours'))
        minutes = int(request.form.get('minutes'))
        difficulty = request.form.get('difficulty')
        mult = int(difficulty)
        min2 = hours * 60
        time = minutes + min2
        money = time * mult * 0.01
        money = round(money, 2)
        new_entry = Entry(cash_add=money, categoryid=categoryid, user_id=current_user.id, difficulty=difficulty, hours=hours, minutes=minutes, category=category)
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
    user = current_user
    if request.method == "POST":
        loss = request.form.get('hhh')
        loss = str(loss)
        loss = float(loss)
        current = user.cash
        current = float(current)
        update = current - loss
        update = round(update, 2)
        if update < 0:
          flash("You don't have that much cash. Sorry!", category="error")
          return redirect("/home")
        categoryid = request.form.get('category')
        cat = CustomType2.query.filter_by(id=categoryid).all()
        for customtype2 in cat:
          category = customtype2.type
        new_remove = Remove(cash_remove=loss, user_id=current_user.id, categoryid=categoryid, category=category)
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
    if request.method == "POST":
        #make_graph1()
      pass
    return render_template("data.html", user=current_user)

@blueprint.route('/custom/s', methods=["GET", "POST"])
@login_required
def custom():
    if request.method == "POST":
        hi = request.form.get("custom")
        new_customtype2 = CustomType2(type=hi, user_id=current_user.id)
        db.session.add(new_customtype2)
        db.session.commit()
        flash("Custom category updated!", category="success")
        return redirect("/custom/s")
    return render_template("custom2.html", user=current_user)

@blueprint.route('/custom/a', methods=["GET", "POST"])
@login_required
def custom2():
    if request.method == "POST":
        it = request.form.get("custom")
        new_entrycat = Entrycat(type=it, user_id=current_user.id)
        db.session.add(new_entrycat)
        db.session.commit()
        flash("Custom category updated!", category="success")
        return redirect("/custom/a")
    return render_template("custom.html", user=current_user)
