"""
TopherAcademy: Mark Ma, Anastasia Lee, Andy Shyklo, Victor Casado
SoftDev
P02: Devo Dining
2025-01-08
Time Spent: 998244353 hours
"""

from flask import Flask, render_template, request, redirect, url_for, session
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
    return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('accountType', None)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/auth_login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if db.checkLogin(email, password) == False:
            return render_template("login.html")
        session['email'] = email
        session['accountType'] = db.checkLogin(email, password)
        return redirect('/')
    return render_template("login.html")
  
@app.route('/restaurants')
def restaurants():
    mode = "manager" # session["mode"]
    name = "bob" # session["name"]
    li = db.getRestaurants()
    return render_template("restaurants.html", mode = mode, name = name, li = li)

# FOR MANAGERS
@app.route('/manage/<restaurant>')
def manage(restaurant):
    return "hi"

# FOR CUSTOMERS
@app.route('/reserve', methods = ['POST'])
def reserve():
    restaurant = request.form['restaurant']
    val = db.getRestaurants()
    to_ret = []
    for x in val:
        if x[0] == restaurant:
            to_ret = x
    time = (to_ret[1], to_ret[2])
    return render_template("reserve.html", restaurant = restaurant, time = time)

@app.route('/makeReservation', methods = ['POST'])
def makeReservation():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
