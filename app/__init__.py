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
        return render_template("home.html")
    return redirect(url_for('logout'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('accountType', None)
    return redirect(url_for('login'))

@app.route('/restaurants')
def restaurants():
    mode = "manager" # session["mode"]
    name = "bob" # session["name"]
    li = db.getRestaurants()
    return render_template("restaurants.html", mode = mode, name = name, li = li)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("AAA")
    if request.method == 'POST':
        print("BBB")
        email = request.form['email']
        password = request.form['password']
        if db.checkLogin(email, password) == False:
            return render_template("login.html")
        session['email'] = email
        session['accountType'] = db.checkLogin(email, password)
        return redirect(url_for(''))
    return render_template("login.html")


def get_times(restaurant, time, numpeople):
    # return a 2d list of [[table ID, time]...]
    return "hi"

# FOR MANAGERS
@app.route('/manage/<restaurant>')
def manage(restaurant):
    return "hi"

# FOR CUSTOMERS
@app.route('/reserve/<restaurant>')
def reserve(restaurant):
    return "hi"

if __name__ == "__main__":
    app.debug = True
    app.run()
