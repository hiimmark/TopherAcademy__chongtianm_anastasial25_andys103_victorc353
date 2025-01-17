"""
TopherAcademy: Mark Ma, Anastasia Lee, Andy Shyklo, Victor Casado
SoftDev
P02: Devo Dining
2025-01-08
Time Spent: 998244353 hours
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
            flash("Invalid login information", 'danger')  # Show error message
            return redirect('/login')
        session['email'] = email
        userType = db.checkLogin(email, password)
        session['accountType'] = userType
        session["restaurant"] = None
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
        session["restaurant"] = None
        return redirect('/')
    return render_template("register.html")

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if session.get("email") == None:
        return redirect("/")
    mode = session['accountType']
    name = session["email"]
    session["restaurant"] = None
    if mode == "customer":
        print("customer")
        li = db.getRestaurants()
    elif mode == "owner":
        print("owner")
        li = db.getRestaurantsOwner(name)
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print(type(li))
        #print(li)
        #print(li[0])
        #print(type(li[0]))
        #print(li[0][0])
        #print(type(li[0][0]))
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
    else:
        return redirect("/logout")
    return render_template("restaurants.html", mode = mode, name = name, li = li)

# FOR OWNERS
@app.route('/manage', methods=['GET', 'POST'])
def manage_post():
    print(1.1)
    if session.get("email") is None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    print(1)
    if session.get("restaurant") == None:
        print(2)
        restaurant1 = request.form.get("restaurant")
        restaurant = db.getRestaurantsInfo(restaurant1)
        session["restaurant"] = restaurant
        print(restaurant)
    else:
        print(3)
        print(session.get("restaurant"))
        restaurant1 = session.get("restaurant")
        #print(restaurant1)
        #print(type(restaurant1))
        #print(restaurant1[0])
        #print(type(restaurant1[0]))
        #print("HEYYYY!!!!")
        #print(restaurant1[0][0])
        #print(type(restaurant1[0][0]))
        restaurant = db.getRestaurantsInfo(restaurant1[0][0])
        session["restaurant"] = restaurant
        #print(restaurant)
        #print(type(restaurant))
        #print("ello mate")
    if not restaurant:
        return "Error: Restaurant name is missing."
    print("hiii")
    print(restaurant)
    print(type(restaurant))
    rest = restaurant[0]
    tablesFromDB = db.getTables(rest[0])
    tables = []
    for table in tablesFromDB:
        tables.append({"id":table[0], "seats":table[1],"x":table[2], "y":table[3]})
    reserve = db.getRestaurantReservations(rest[0])
    #print(reserve)
    #print(type(reserve))
    #print(reserve[0])
    #print(type(reserve[0]))
    #print(reserve[1])
    #print(type(reserve[1]))
    #print(reserve[0][0])
    #print(type(reserve[0][0]))
    #print("iujqsod8qyuwoik")
    return render_template("manage.html", rest = rest, tables = tables, reserve = reserve)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if session.get("email") is None:
        return redirect("/")
    if session.get("accountType") == "customer":
        return redirect("/restaurants")
    restaurant = request.form.get("new_val")
    print(restaurant)
    new_val = request.form.get("new_val")
    field_name = request.form.get("val")
    num = request.form.get("num")
    restA = new_val.split(",")
    if (num == 2 or num == "2"):
        print(f"lsdds: {field_name}")
        print(type(field_name))
        print(restA[0][2:-1])
        print(type(restA[0][2:-1]))
        ls = db.updateRestaurantOpen(restA[0][2:-1], field_name)
        print(f"ls: {ls}")
    print(f"time{field_name} ttoal {new_val} num {num}")
    return redirect("/manage")

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
# FOR MANAGERS
# @app.route('/manage', methods=['GET', 'POST'])
# def manage():
#     if session.get("email") == None:
#         return redirect("/")
#     if session.get("accountType") == "customer":
#         return redirect("/restaurants")

#     if request.method == "POST":
#         restaurant=request.form['restaurant']
#         tablesFromDB = db.getTables(restaurant)
#         tables = []
#         for table in tablesFromDB:
#             tables.append({"id":table[0], "x":table[2], "y":table[3]})
#         return render_template("drag.html", restaurant=restaurant, tables=tables)

#     return redirect("/logout") #should never go here

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
    time = [to_ret[1], to_ret[2]]
    if len(time[0]) == 4:
        time[0] = "0" + time[0]
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
    return render_template("available_tables.html", date = date, time = time, num = num, restaurant = restaurant, tables = tables)

@app.route('/add_table', methods=['POST'])
def add_table():
    try:
        data = request.get_json()
        response = {'message': 'Table added successfully'}

        print(data)
        restaurant = data.get("restaurant_name")
        print("HEWWWOO")
        print(restaurant)
        x = data.get("x")
        y = data.get("y")
        seats = data.get("seats")
        f = db.createTable(restaurant, seats, x, y)
        print(f"ASHDIASGDFIYUQWUQHIUH {f}")

        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/makeReserve', methods=['POST'])
def makeReserve():
    try:
        data = request.get_json()
        response = {'success': True}

        print(data)
        tableID = int(data.get("table_id"))
        email = session.get("email")
        num = int(data.get("num"))
        time = (data.get("date")+'-'+data.get("time"))
        db.createReservation(email, tableID, num, time)

        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    app.debug = True
    app.run()
