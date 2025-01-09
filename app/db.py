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
def resetDB():
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print("Resetting DB")
        createTables()
    else:
        print("Cannot reset database as database does not exist")

 #returns true if successful, and false if not (email is identical to another user's)
 #all inputs are strings
def createUser(email, password, type):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()

    try:
        c.execute('INSERT INTO UserData VALUES (?, ?, ?)', (email, password, type))
        db.commit()
        db.close()
        print("Successfully added user")
        return True
    except Exception as e:
        print("Failed to add user")
        db.close()
        return False

#openTime, closeTime as strings in military time (14:20), timeBetweenReserves integer in minutes, owner is the owner's email
#name is also a string
#returns true if successful, and false if not (name is identical to another restaurant's)
def createRestaurant(name, openTime, closeTime, timeBetweenReserves, owner):
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
#0 if table ID provided does not exist
#6 if there are not enough seats at the requested table
#2 if the table is not linked to a Restaurant
#3 if the restaurant is not open at the requested time
#4 if another reservation is too close in time
#5 if an error occurs while inserting into the db
#use output == True to check if its an integer or boolean (1 is not an output b/c 1==True is True in python)
def createReservation(reserverEmail, tableID, numPeople, time):
    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    c.execute("SELECT restaurant, numSeats FROM TableData WHERE ID = ?", (tableID,))
    row = c.fetchone()

    if row == None:
        print("Reservation failed because the table does not exist")
        return 0 #no such table

    if numPeople > row[1]:
        print("Reservation failed due to a lack of seats at requested table")
        return 6 #not enough seats

    wantedTime = datetime.strptime(time, "%Y-%m-%d-%H:%M")

    c.execute("SELECT openTime, closeTime, timeBetweenReserves FROM RestaurantData WHERE name = ?", (row[0],))
    row = c.fetchone()

    if row == None:
        print("Reservation failed because no restaurant exists for said table")
        return 2 #the table doesnt have a restaurant?

    start_time = datetime.strptime(row[0], "%H:%M").time()
    end_time = datetime.strptime(row[1], "%H:%M").time()

    if not (start_time <= wantedTime.time() <= end_time):
        print("Reservation failed because restaurant is not open at requested time")
        return 3 #restaurant is not open

    timeDistance = timedelta(minutes=row[2])

    c.execute("SELECT time FROM ReservationData WHERE tableID = ?", (tableID,))
    timesReserved = c.fetchall()

    for reservation in timesReserved:
        reservationTime = datetime.strptime(reservation[0], "%Y-%m-%d-%H:%M")
        if(abs(wantedTime - reservationTime) < timeDistance):
            print("Reservation failed because another reservation is too close time-wise")
            return 4 #another reservation too close

    try:
        c.execute("INSERT INTO ReservationDATA VALUES (?, ?, ?, ?)", (reserverEmail, tableID, numPeople, time))
        db.commit()
        db.close()
        print("Reservation Added Successfully")
        return True
    except:
        print("Reservation Failed??")
        return 5
'''
resetDB()
print(createUser("joe", "smith", "owner"))
print(createRestaurant("pizzaAAAA RUN", "8:40", "13:10", 12, "joe"))
print(createTable("pizzaAAAA RUN", 8))
print(createReservation("mr smith", 1, 6, "2024-12-17-12:07"))
print(createReservation("mr smith", 1, 7, "2024-12-17-12:07"))
print(createReservation("mr smith", 1, 7, "2024-12-17-8:07"))
'''
