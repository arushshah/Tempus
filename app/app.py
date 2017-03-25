from flask import Flask, render_template, request, session, redirect, make_response
import mysql.connector
import os

app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="public")

cur = conn.cursor()
@app.route("/")
def index():
	if not session.get('logged_in'):
		return render_template("index.html")
	else:
		return redirect("/calendar")

@app.route("/login", methods=["POST"])
def login():

	username = request.form['username']
	password = request.form['password']
	print(username)
	print(password)
	query = 'SELECT * FROM users'
	cur.execute(query)

	users = cur.fetchall()
	userIndex = -1;

	for i in range (0, len(users)):
		if (username in users[i]):
			userIndex = i
			break
	if (password in users[i]):
		session['logged_in'] = True
		resp = make_response(redirect("/calendar"))
		resp.set_cookie("username", username)
		resp.set_cookie("firstName", users[i][1])
		return resp
	else:
		return render_template("index.html", message = "Username or Password Incorrect")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/newaccount", methods=["POST"])
def newaccount():
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	username = request.form['username']
	password = request.form['password']

	if (len(firstName) == 0 or len(lastName) == 0 or len(username) == 0 or len(password) == 0):
		return render_template("register.html", message="One or more fields is empty.")

	query='SELECT * FROM users where username LIKE "%s"' % username
	cur.execute(query)

	if (len(cur.fetchall()) != 0):
		return render_template("register.html", message="Username already exists.")

	query = 'INSERT INTO users (firstName, lastName, username, password) VALUES ("%s", "%s", "%s", "%s")' % (firstName,lastName,username,password)
	cur.execute(query)
	conn.commit()

	return render_template("index.html", message="Account created! Please log in.")

@app.route("/calendar")
def calendar():
	if session.get('logged_in'):
		return render_template("calendar.html")
	else:
		return render_template("index.html", message="Please log in to access calendar.")

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect("/")

@app.route("/addtask")
def addtask():
	if session.get('logged_in'):
		return render_template("addtask.html")
	else:
		return render_template("index.html", message="Please log in to add tasks.")


@app.route("/newtask", methods=["POST"])
def newtask():
	taskName = request.form['taskName']
	dueDate = request.form['dueDate']
	timeNeeded = request.form['timeNeeded']

	if (len(taskName) == 0 or len(str(dueDate)) == 0 or len(str(timeNeeded)) == 0 ):
		return render_template("addtask.html", message="One or more fields is empty.")

	print(taskName)
	print(dueDate)
	print(timeNeeded)

	query = 'INSERT INTO tasks (taskName, dueDate, approxTime, username) VALUES ("%s", STR_TO_DATE("%s", "%%Y-%%m-%%d"), "%s", "%s")' % (taskName, dueDate, timeNeeded, request.cookies.get("username"))
	print(query)
	cur.execute(query)
	conn.commit()

	return redirect("/calendar")

@app.route("/todaystasks")
def todaystasks():
	if session.get('logged_in'):
		query = 'SELECT * FROM tasks WHERE username LIKE "%s"' % request.cookies.get("username")
		cur.execute(query)

		return render_template("todaytasks.html", tasks=cur.fetchall())
	else:
		return render_template("index.html", message="Please log in to access your tasks.")

if __name__ == "__main__":
	app.secret_key = os.urandom(24)
	app.run(debug=True)