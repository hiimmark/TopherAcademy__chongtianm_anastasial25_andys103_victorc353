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

db.createSampleData()

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
            flash("Invalid login information", 'danger')  # Show error message
            return redirect('/login')
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
            flash("Invalid: Account exists already", 'danger')  # Show error message
            return redirect('/register')
        session['email'] = email
        session['accountType'] = usty
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

# FOR OWNERS
@app.route('/manage', methods=['POST'])
def manage_post():
    if session.get("email") is None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    restaurant = request.form.get("restaurant")
    if not restaurant:
        return "Error: Restaurant name is missing."
    print(restaurant)
    rest = restaurant[1:-1].split(",")
    print(type(restaurant))
    print(rest)
    print(type(rest))
    restA = []
    a = 0
    for (i) in rest:
        if a == 0:
            restA.append(i[1:-1])
        else:
            restA.append(i[2:-1])
        print(f"hi: {i}")
        a += 1
    
    return render_template("manage.html", rest = restA)

# FOR MANAGERS
#@app.route('/manage/<restaurant>', methods=['GET', 'POST'])
#def manage(details):
#    if session.get("email") == None:
#        return redirect("/")
#    if session.get("accountType") == "customer":
#        return redirect("/restaurants")
#    # details = db.getRestaurantsInfo(restaurant)
#    if not details:
#        return redirect("/restaurants")
#    return render_template("manage.html", rest = details)

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
            flash("Error: Could not create the restaurant. Please try again.", 'danger')
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
    cur_date = datetime.today().strftime('%Y-%m-%d')
    return render_template("reserve.html", restaurant = restaurant, time = time, date = cur_date)

@app.route('/makeReservation', methods = ['GET', 'POST'])
def makeReservation():
    if session.get("email") == None:
        return redirect("/")
    time = request.form['time']
    num = request.form['num']
    restaurant = request.form["restaurant"]
    date = request.form['date']
    tables = db.getAvailableTables(restaurant, int(num), date+'-'+time)
    for i in range(len(tables)):
        tables[i].append(i+1)
    return render_template("make_reservation.html", date = date, time = time, num = num, restaurant = restaurant, tables = tables)

@app.route('/reserveTable', methods = ['POST'])
def reserveTable():
    time = request.form['time']
    date = request.form['date']
    table = request.form['table']
    num = request.form['num']
    res = db.createReservation(session['email'], table, int(num), date+"-"+time)
    return render_template("reserve_table.html", resp = res)

if __name__ == "__main__":
    app.debug = True
    app.run()
