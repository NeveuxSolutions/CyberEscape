from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import re
from multiprocessing import Value

#-------------------
# Configuration
#-------------------
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SECRET_KEY'] = "g5ac358c-f0bf-11e5-9e39-d3b532c10a28"
db = SQLAlchemy(app)
lives = Value('i', 3)

#-------------------
# Database Model
#-------------------
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(20), unique=True, nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = password

# Drop/Create all Tables
db.drop_all()
db.create_all()
user = User('Ma3ve', 'clementine')
db.session.add(user)
db.session.commit()

#-------------------
# Routes
#-------------------

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/begin')
def begin():
	return render_template('begin.html')

@app.route('/error')
def error():
	return render_template('error.html')

@app.route('/wrong_password')
def wrong_password():
	return render_template('wrong_password.html')

@app.route('/gameover')
def gameover():
	return render_template('gameover.html')

@app.route('/logged_in')
def logged_in():
	if session.get('admin') == True:
		return redirect(url_for('admin'))
	return render_template('logged_in.html', user=session.get('username'))
 
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['name']
		password = request.form['password']
		vulnerability_list = ["' or 1=1--", "' or 1=1#", "' or 1=1/*"]
		if username == 'Ma3ve' and password not in vulnerability_list and password != 'clementine':
			return redirect(url_for('wrong_password'))
		if password in vulnerability_list:
			password = 'clementine'

		# Create user session
		session['username'] = username
		session['password'] = password
		session['admin'] = True
		user = User.query.filter(User.password == password, User.username == username).first()
		if user == None:
			return redirect(url_for('error'))
		else:
			return redirect(url_for('logged_in'))
	return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if session.get('admin') != True:
		return redirect(url_for('login'))
	if request.method == 'POST':
		form_data = request.form['form_submit']
		find_false = re.search(r"\'obey_humans'\:\sFalse", form_data)
		if find_false:
			return render_template('success.html')
		else:
			with lives.get_lock():
				lives.value -= 1
				if lives.value <= 0:
					lives.value = 3
					return redirect(url_for('gameover'))
				flash(f'ERROR: Main Systems still functional. You have {lives.value} more attempts')
				return redirect(url_for('admin'))
	return render_template('admin.html')		

#-------------------
# Main
#-------------------
if __name__ == '__main__':
	app.run(debug = True)
	