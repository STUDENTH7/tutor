import flask
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = '_KEY'


def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query1 = ("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname text, "
                  "surname text, username text, phonenumber text, email text, password text, role text);")

        query2 = ("CREATE TABLE IF NOT EXISTS GRADES (id INTEGER PRIMARY KEY AUTOINCREMENT, student text, "
                  "course text, marks integer, grade text);")
        cursor.execute(query1)
        cursor.execute(query2)
        conn.commit()
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def list_data(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM person"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def save_data(filename, firstname, surname, username, phonenumber, email, password, role):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query3 = "INSERT INTO person (firstname, surname, username, phonenumber, email, password, role) values ('" + firstname + "','" + surname + "','" + username + "','" + phonenumber + "','" + email + "','" + password + "','" + role + "')"
        print(query3)
        result = cursor.execute(query3)
        conn.commit()
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def list_GRADE_data(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM GRADES"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def save_GRADE_data(filename, student, course, marks, grade):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query4 = "INSERT INTO GRADES (student, course, marks, grade) values ('" + student + "','" + course + "','" + marks + "','" + grade + "');"
        print(query4)
        result = cursor.execute(query4)
        conn.commit()
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


@app.route('/')
def home():
    create_sqlite_database("user.db")
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/books_resources')
def books_resources():
    return render_template("books_resources.html")


@app.route('/courses')
def courses():
    return render_template("courses.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    user_exists, user_role = login_user("user.db", username, password)

    if user_exists == "valid" and user_role == "student":

        flask.session["username"] = username
        return redirect(url_for("studentMAIN"))

    elif user_exists == "valid" and user_role == "tutor":
        flask.session["username"] = username
        return redirect(url_for("tutorMAIN"))
    else:
        return render_template("login.html", status="Invalid username or password, try again")


# Function to log in a user
def login_user(filename, username, password):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            return "valid", user[7]

        else:
            return "invalid", None
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


@app.route('/forgotpasswords')
def forgot():
    return render_template("forgotpasswords.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


#tutor stuff
@app.route('/TUTOR_SIGNUP')
def tutorsignup():
    return render_template("TUTOR_SIGNUP.html")


@app.route("/TUTOR_SIGNUP", methods=['POST'])
def TUTORsignup_post():
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    username = request.form["username"]
    phonenumber = request.form["phonenumber"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]
    save_data("user.db", firstname, surname, username, phonenumber, email, password, role)
    return render_template("login.html", person_data=list_data("user.db"))


@app.route('/TUTOR_MAIN')
def tutorMAIN():
    username = session.get('username')
    LEADB = Leaderboard('user.db')
    print(LEADB)
    STU = []
    MARKS = []
    for u in LEADB:
        STU.append(u[0])
        MARKS.append(u[1])
    plot2 = get_lead(STU, MARKS)
    plot2.savefig(os.path.join('static', 'images', 'plot3.png'))

    return render_template("TUTOR_MAIN.html", logged_in_tutor=username, listed_tutor=list_TUTOR('user.db', username),
                           sdata=list_data('user.db'), gdata=list_GRADE_data('user.db'))


@app.route("/TUTOR_MAIN", methods=['POST'])
def TUTORMAIN_post():
    username = session.get('username')
    student = request.form["student"]
    course = request.form["course"]
    marks = request.form["marks"]
    grade = request.form["grade"]
    save_GRADE_data("user.db", student, course, marks, grade)
    print(list_GRADE_data("user.db"))

    return render_template("TUTOR_MAIN.html", sdata=list_data('user.db'),
                           logged_in_tutor=username, listed_tutor=list_TUTOR('user.db', username),
                           gdata=list_GRADE_data('user.db'))


def list_TUTOR(filename, username):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM person WHERE username='" + username + "'"
        result = cursor.execute(query)
        data = result.fetchone()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


#student stuff
@app.route('/STUDENT_SIGNUP')
def studentsignup():
    return render_template("STUDENT_SIGNUP.html")


@app.route("/STUDENT_SIGNUP", methods=['POST'])
def STUDENTsignup_post():
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    username = request.form["username"]
    phonenumber = request.form["phonenumber"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]
    save_data("user.db", firstname, surname, username, phonenumber, email, password, role)
    return render_template("login.html", person_data=list_data("user.db"))


def get_plot(course, marks):
    x = np.array(course)
    y = np.array(marks)
    plt.bar(x, y)
    return plt

def get_lead(student, marks):
    x = np.array(student)
    y = np.array(marks)
    plt.bar(x, y)
    return plt

@app.route('/STUDENT_MAIN')
def studentMAIN():
    username = session.get('username')
    tg=total_STUDENT_grades('user.db', username)
    print(tg)
    lstcourse=[]
    lstmarks = []
    for u in tg:
        lstcourse.append(u[0])
        lstmarks.append(u[1])
    plot = get_plot(lstcourse, lstmarks)
    plot.savefig(os.path.join('static', 'images', 'plot1.png'))

    LEADB = Leaderboard('user.db')
    print(LEADB)
    STU = []
    MARKS = []
    for u in LEADB:
        STU.append(u[0])
        MARKS.append(u[1])
    plot2 = get_lead(STU, MARKS)
    plot2.savefig(os.path.join('static', 'images', 'plot3.png'))

    return render_template("STUDENT_MAIN.html", logged_in_student=username,
                           listed_student=list_STUDENT('user.db', username),
                           Studentgrades=list_STUDENT_grades('user.db', username),
                           Total_Grades=total_STUDENT_grades('user.db', username))


def list_STUDENT(filename, username):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM person WHERE username='" + username + "'"
        result = cursor.execute(query)
        data = result.fetchone()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def list_STUDENT_grades(filename, username):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT * FROM GRADES WHERE student='" + username + "'"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def total_STUDENT_grades(filename, username):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT course, sum(marks) FROM GRADES WHERE student='" + username + "'" + " GROUP BY course"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


def Leaderboard(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        query = "SELECT student, sum(marks) FROM GRADES GROUP BY student ORDER BY marks DESC"
        result = cursor.execute(query)
        data = result.fetchall()
        conn.commit()
        return data
    except sqlite3.Error as e:
        return e
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run()

