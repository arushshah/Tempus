from flask import Flask, render_template, request, redirect, make_response
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="public")

cur = conn.cursor()
@app.route("/")
def index():
	print(request.cookies.get("username"))
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	print("LOGIN CALLED")
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
		'''resp = redirect("/home")
		resp.set_cookie("username", username)
		resp.set_cookie("firstName", users[i][1])
		resp.set_cookie("lastName", users[i][2])
		return resp'''
		return redirect("/calendar")
	else:
		print("Not")
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
	return render_template("calendar.html")

if __name__ == "__main__":
	app.run(debug=True)