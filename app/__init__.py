"""
TopherAcademy: Mark Ma, Anastasia Lee, Andy Shyklo, Victor Casado
SoftDev
P02: Devo Dining
2025-01-08
Time Spent: 998244353 hours
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import calendar, os
from datetime import datetime
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# HOME PAGE, SHOULD PROMPT REGISTER OR LOGIN

@app.route('/', methods=['GET', 'POST'])
def homeBase():
    if('accountType' in session):
        return redirect('/restaurants')
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    session.pop('accountType', None)
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("")
    return render_template("login.html")

@app.route('/auth_login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if db.checkLogin(email, password) == False:
            message = "Incorrect Login information"
            return render_template("login.html", message = message)
        session['email'] = email
        userType = db.checkLogin(email, password)
        session['accountType'] = userType
        return redirect('/')
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/auth_register', methods=['GET', 'POST'])
def auth_register():
    if request.method == 'POST':
        usty = request.form['userType']
        email = request.form['email']
        password = request.form['password']
        if db.createUser(email, password, usty) == False:
            message = "Invalid information: Account exists already"
            return render_template("register.html", message = message)
        if db.checkLogin(email, password) == False:
            message = "Incorrect Login information"
            return render_template("login.html", message = message)
        session['email'] = email
        userType = db.checkLogin(email, password)
        session['accountType'] = userType
        return redirect('/')
    return render_template("register.html")

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if session.get("email") == None:
        return redirect("/")
    mode = session['accountType']
    name = session["email"]
    if mode == "customer":
        print("customer")
        li = db.getRestaurants()
    elif mode == "owner":
        print("owner")
        li = db.getRestaurantsOwner(name)
    else:
        return redirect("/logout")
    return render_template("restaurants.html", mode = mode, name = name, li = li)

# FOR MANAGERS
@app.route('/manage/<restaurant>', methods=['GET', 'POST'])
def manage(restaurant):
    if session.get("email") == None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    return "hi"

@app.route('/create', methods=['GET', 'POST'])
def create():
    if session.get("email") == None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    return render_template("create.html")

@app.route('/creator', methods=['GET', 'POST'])
def creator():
    if session.get("email") == None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    if request.method == 'POST':
        name = request.form['name']
        open = request.form['open']
        close = request.form['close']
        between = request.form['between']
        owner = session["email"]
        if db.createRestaurant(name, open, close, between, owner):
            return redirect("/restaurants")
        else:
            flash("Error: Could not create the restaurant. Please try again.")
            return redirect("/create")
    return redirect("/restaurants")

# FOR CUSTOMERS
@app.route('/reserve', methods = ['GET', 'POST'])
def reserve():
    if session.get("email") == None:
        return redirect("/")
    restaurant = request.form['restaurant']
    val = db.getRestaurants()
    to_ret = []
    for x in val:
        if x[0] == restaurant:
            to_ret = x
    time = (to_ret[1], to_ret[2])
    return render_template("reserve.html", restaurant = restaurant, time = time)

@app.route('/makeReservation', methods = ['GET', 'POST'])
def makeReservation():
    if session.get("email") == None:
        return redirect("/")
    time = request.form['time']
    num = request.form['num']
    restaurant = request.form["restaurant"]
    return render_template("make_reservation.html", restaurant = restaurant)

if __name__ == "__main__":
    app.debug = True
    app.run()
