import flask
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
import requests
import re



# APIKEY = 1d6c838926cb4ee8ba1100056252401

# we need a key for the sql stuff/saving data
app = Flask(__name__)



def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query1 = ("CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT,Firstname text, "
                  "Lastname text, Username text, Email text, Password text);")
        cursor.execute(query1)
        conn.commit()
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def LIST_USERS(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM USERS"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def SAVE_USERS(filename, Firstname, Lastname, Username, Email, Password):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query3 = "INSERT INTO USERS ( Firstname, Lastname, Username, Email, Password) values ('" + Firstname + "','" + Lastname + "','" + Username + "','" + Email + "','" + Password + "')"
        print(query3)
        result = cursor.execute(query3)
        conn.commit()
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


# the app route allows the html to display
@app.route('/')
def home():
    create_sqlite_database("USERS.db")
    return render_template("HOME.html")


@app.route('/TICKETS')
def TICKETS():
    return render_template("TICKETS.html")


@app.route('/HOTEL')
def HOTEL():
    return render_template("HOTEL.html")


@app.route('/ZOO')
def ZOO():
    return render_template("ZOO.html")

@app.route('/MEMBERS')
def MEMBERS():
    return render_template("MEMBERS.html")

@app.route('/ABOUT')
def ABOUT():
    return render_template("ABOUT.html")


@app.route('/LOGIN')
def LOGIN():
    return render_template("LOGIN.html")


# this is after the function for users to be able to login after inputting their username nd password
@app.route('/LOGIN', methods=['GET', 'POST'])
def LOGIN_POST():
    # fetches the username and password form database and compares them to what user has inputted
    Username = request.form["Username"]

    Password = request.form["Password"]

    user_exist = LOGINUser("USERS.db", Username, Password)

    if user_exist == "valid":

        flask.session["Username"] = Username
        return redirect(url_for("LOGGED"))


    else:

        # validation on their login (it gives you an error message is username and password is incorrect)
        return render_template("LOGIN.html", status="Invalid username or password, try again")


# sql query for login
def LOGINUser(filename, Username, Password):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE Username = ? AND Password = ?", (Username, Password))
        user = cursor.fetchone()

        # validtion
        if user:
            return "valid", user[6]

        else:
            return "invalid", None
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


@app.route('/FOPAS')
def fopas():
    return render_template("FORGOTPASSWORD.html")


@app.route('/SIGNUP')
def SIGNUP():
    return render_template("SIGNUP.html")


@app.route('/SIGNUP', methods=['POST'])
def SIGNUP_POST():
    Firstname = request.form["Firstname"]
    Lastname = request.form["Lastname"]
    Username = request.form["Username"]
    Email = request.form["Email"]
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", Email):
        return render_template("SIGNUP.html", status="invalid email")
    else:
        print("Valid email address." if valid else "Invalid email address")
        Password = request.form["Password"]
        Gender = request.form["Gender"]
        SAVE_USERS("USERS.db", Firstname, Lastname, Username, Email, Password, Gender)
        return render_template("LOGIN.html", PEOPLE=LIST_USERS("USERS.db"))


@app.route('/LOGGED_MAIN')
def LOGGED():
    Username = session.get('Username')
    return render_template("LOGGED.html",
                           Logged_name=Username, listed=Log_user('USERS.db', Username))




def Log_user(filename, Username):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM USERS WHERE Username='" + Username + "'"
        result = cursor.execute(query)
        data = result.fetchone()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()




if __name__ == '__main__':
    app.run()

    check(email)


