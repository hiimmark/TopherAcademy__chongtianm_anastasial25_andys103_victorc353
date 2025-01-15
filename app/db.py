import sqlite3, os
from datetime import datetime, time, timedelta

DATABASE_NAME = "DATABASE.db"

def createTables():
    if os.path.exists(DATABASE_NAME):
        print("Database already exists!!!\nWill not create tables")
    else:
        print("Creating tables...")
        db = sqlite3.connect(DATABASE_NAME)
        c = db.cursor()

        #User Info
        c.execute('''
                CREATE TABLE IF NOT EXISTS UserData (
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    type TEXT)
            ''')

        #Restaurant Info
        c.execute('''
                CREATE TABLE IF NOT EXISTS RestaurantData (
                    name TEXT UNIQUE NOT NULL,
                    openTime TEXT NOT NULL,
                    closeTime TEXT NOT NULL,
                    timeBetweenReserves INTEGER NOT NULL,
                    owner TEXT NOT NULL)
            ''') #timeBetweenReserves in minutes
                # openTime and closeTime in military time (13:10 is 1:10 PM)

        #Table Info
        c.execute('''
                CREATE TABLE IF NOT EXISTS TableData (
                    ID INTEGER PRIMARY KEY,
                    restaurant TEXT NOT NULL,
                    numSeats INTEGER NOT NULL)
            ''')

        #Reservation Info
        c.execute('''
                CREATE TABLE IF NOT EXISTS ReservationData (
                    reserverEmail TEXT NOT NULL,
                    tableID TEXT NOT NULL,
                    numPeople INTEGER NOT NULL,
                    time TEXT NOT NULL)
            ''') #time in military time (13:10 is 1:10 PM)

        db.commit()
        db.close()

        print("Tables successfully created \n")
        return True

#just call this when resetting db, it calls createTables
#if not, call neither
def resetDB():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("Resetting DB")
        return createTables()
    else:
        print("Cannot reset database as database does not exist")
        print("Creating database")
        return createTables()

 #returns true if successful, and false if not (email is identical to another user's)
 #all inputs are strings
 #owner account = "owner", customer account = "customer"
def createUser(email, password, type):
    print(f"Adding user {email}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()

    try:
        c.execute('INSERT INTO UserData VALUES (?, ?, ?)', (email, password, type))
        db.commit()
        db.close()
        print("Successfully added user")
        return True
    except Exception as e:
        print("Failed to add user (does the user already exist in the database?)")
        db.close()
        return False

#openTime, closeTime as strings in military time (14:20), timeBetweenReserves integer in minutes, owner is the owner's email
#name is also a string
#returns true if successful, and false if not (name is identical to another restaurant's)
def createRestaurant(name, openTime, closeTime, timeBetweenReserves, owner):
    print(f"Creating restaurant {name} which opens at {openTime}, closes at {closeTime}, needs {timeBetweenReserves} minutes between reservations, and is owned by {owner}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()

    try:
        c.execute('INSERT INTO RestaurantData VALUES (?, ?, ?, ?, ?)', (name, openTime, closeTime, timeBetweenReserves, owner))
        db.commit()
        db.close()
        print("Successfully added restaurant")
        return True
    except Exception as e:
        print("Failed to add restaurant")
        db.close()
        return False

#restaurant is string name of restaurant, numSeats is integer
#returns true if successful, false if not (don't know why it wouldn't be)
def createTable(restaurant, numSeats):
    print(f"Creating table with {numSeats} seats at {restaurant}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()

    try:
        c.execute('INSERT INTO TableData (restaurant, numSeats) VALUES (?, ?)', (restaurant, numSeats))
        db.commit()
        db.close()
        print("Successfully added table")
        return True
    except Exception as e:
        print(e)
        print("Failed to add table")
        db.close()
        return False

#reserverEmail, time are strings, tableID, numPeople are integers
#time is a string in the form "2024-12-27-13:10"
#returns true if successful, integer if not
#String explaining error to user if unsuccesful
#use output == True to check if its an integer or boolean (1 is not an output b/c 1==True is True in python)
def createReservation(reserverEmail, tableID, numPeople, time):
    print(f"Creating reservation for {reserverEmail} at table {tableID} for {numPeople} people at {time}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT restaurant, numSeats FROM TableData WHERE ID = ?", (tableID,))
    row = c.fetchone()

    if row == None:
        print("Reservation failed because the table does not exist")
        return "Something went wrong"

    if numPeople > row[1]:
        print("Reservation failed due to a lack of seats at requested table")
        return "Not enough seats at requested table"

    wantedTime = datetime.strptime(time, "%Y-%m-%d-%H:%M")

    c.execute("SELECT openTime, closeTime, timeBetweenReserves FROM RestaurantData WHERE name = ?", (row[0],))
    row = c.fetchone()

    if row == None:
        print("Reservation failed because no restaurant exists for said table")
        return "Something went wrong"

    start_time = datetime.strptime(row[0], "%H:%M").time()
    end_time = datetime.strptime(row[1], "%H:%M").time()

    if not (start_time <= wantedTime.time() <= end_time):
        print("Reservation failed because restaurant is not open at requested time")
        return "Restaurant is not open at selected time"

    timeDistance = timedelta(minutes=row[2])

    c.execute("SELECT time FROM ReservationData WHERE tableID = ?", (tableID,))
    timesReserved = c.fetchall()

    for reservation in timesReserved:
        reservationTime = datetime.strptime(reservation[0], "%Y-%m-%d-%H:%M")
        if(abs(wantedTime - reservationTime) < timeDistance):
            print("Reservation failed because another reservation is too close time-wise")
            return "Another user has requested this table at a similar time"

    try:
        c.execute("INSERT INTO ReservationDATA VALUES (?, ?, ?, ?)", (reserverEmail, tableID, numPeople, time))
        db.commit()
        db.close()
        print("Reservation Added Successfully")
        return True
    except:
        print("Reservation failed while adding to DB")
        return "Something went wrong"

#Returns list of tuples
#Each tuple has (name, openTime, closeTime, timeBetweenReserves, owner)
def getRestaurants():
    print("Getting all restaurants")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT name, openTime, closeTime, timeBetweenReserves, owner FROM RestaurantData")
    return c.fetchall()

def getRestaurantsInfo(name):
    print(f"Getting Info of Restaurant {name}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT name, openTime, closeTime, timeBetweenReserves, owner FROM RestaurantData WHERE name = ?", (name,))
    return c.fetchall()

#Returns list of tuples
#Each tuple has (name, openTime, closeTime, timeBetweenReserves, owner)
#Only selects from values where the owner is selected
def getRestaurantsOwner(owner):
    print("Getting all restaurants")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT name, openTime, closeTime, timeBetweenReserves, owner FROM RestaurantData WHERE owner = ?", (owner,))
    return c.fetchall()

#restaurant is string (name of restaurant)
#Returns list of tuples
#Each tuple has (ID, numSeats)
def getTables(restaurant):
    print(f"Getting all tables for {restaurant}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT ID, numSeats FROM TableData WHERE restaurant = ?", (restaurant,))
    return c.fetchall()

#restaurant is integer (ID of table)
#Returns list of tuples
#Each tuple has (reserverEmail, numPeople, timeReserved, tableID)
def getReservations(tableID):
    print(f"Getting all reservations for table {tableID}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT reserverEmail, numPeople, time, tableID FROM ReservationData WHERE tableID = ?", (tableID,))
    return c.fetchall()

#name is name of restaurant
#returns 2d list
#[[reservations for first table in restaurant], [reservations for second table in restaurant], [etc]]
#reservations for each table is a list in the form [reserverEmail, numPeople, timeReserved, tableID]
def getRestaurantReservations(name):
    print(f"Getting all reservations for {name}")
    tables = getTables(name)
    reservations = []
    for i in tables:
        reservations.append(getReservations(i[0]))
    return reservations

#email and password are text
#returns user type if correct
#returns False if login incorrect / does not exist
def checkLogin(email, password):
    print(f"Checking login for {email}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT password, type FROM UserData WHERE email = ?", (email,))
    row = c.fetchone()

    if row == None:
        print("Email does not exist in db")
        return False #account w that email does not exist

    if row[0] == password:
        print("Login correct")
        return row[1]
    else:
        print("Incorrect password")
        return False

#tableID is integer (ID of table)
#removes specified table from database
#returns true (or false if something unexpected goes wrong)
def delTable(tableID):
    print(f"Deleting table {tableID}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    try:
        c.execute("DELETE FROM TableData WHERE ID = ?", (tableID,))
        print(f"Deleting reservations at table {tableID} as we are removing the table")
        c.execute("DELETE FROM ReservationData WHERE tableID = ?", (tableID,))
        db.commit()
        db.close()
        return True
    except Exception as e:
        print("Something went wrong")
        return False

#tableID is integer (ID of table that reservation is at)
#time is string in the form "2024-12-27-13:10"
#returns true (or false if something unexpected goes wrong)
def delReservation(tableID, time):
    print(f"Deleting reservation at table {tableID} at {time}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    try:
        c.execute("DELETE FROM ReservationData WHERE (tableID, time) = (?, ?)", (tableID, time))
        db.commit()
        db.close()
        return True
    except:
        print("Something went wrong")
        return False

#name is string of restaurant
#returns true (or false if something unexpected goes wrong)
def delRestaurant(name):
    print(f"Deleting restaurant {name}")
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    try:
        c.execute("DELETE FROM RestaurantData WHERE name = ?", (name,))
        db.commit()
        db.close()
        tables = getTables(name)
        print(f"Deleting tables from {name}")
        for table in tables:
            ID = table[0]
            delTable(ID)
        return True
    except:
        print("Something went wrong")
        return False

#will reset DB and add some data
def createSampleData():
    resetDB()
    createUser("topher@hotmail.com", "mykolyk", "owner")
    createUser("tberri50@stuy.edu", "instructorendorsed", "owner")
    createRestaurant("#GUDFAM Bagels", "8:00", "15:00", 20, "topher@hotmail.com")
    createRestaurant("Berri's Berry Smoothies", "7:00", "20:00", 30, "tberri50@stuy.edu")
    createTable("#GUDFAM Bagels", 10)
    createTable("#GUDFAM Bagels", 3)
    createTable("#GUDFAM Bagels", 5)
    createTable("Berri's Berry Smoothies", 1)
    createTable("Berri's Berry Smoothies", 2)
    createTable("Berri's Berry Smoothies", 4)
    createUser("marge@stuy.edu", "cslab", "customer")
    createReservation("marge@stuy.edu", 1, 2, "2025-6-27-11:10")
    createReservation("marge@stuy.edu", 1, 2, "2025-6-27-13:10")
    createReservation("marge@stuy.edu", 2, 3, "2025-6-27-14:10")

#restaurant is restaurant's name, numPeople is number of people for the reservation, numPeople is the number of people
#time is a string in the form "2024-12-27-13:10"
#returns list of [tableID, numSeats] of available tables
def getAvailableTables(restaurant, numPeople, time):
    returner = []
    tables = getTables(restaurant)
    for table in tables:
        if table[1] >= numPeople:
            if createReservation("checking if works", table[0], numPeople, time):
                returner.append([table[0], table[1]])
            delReservation(table[0], time)
    return returner
