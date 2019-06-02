from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(20))

	def __init__(self, username, password):
		self.username = username
		self.password = password

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/begin')
def begin():
	return render_template('begin.html')

@app.route('/tables')
def tables():
	return render_template('tables.html', User=User.query.filter_by(email='fuck@email.com'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['name']
		password = request.form['password']
		vulnerability_list = ["' or 1=1--", "' or 1=1#", "' or 1-1/*"]
		if password in vulnerability_list:
			password = 'clementine'
		return render_template('tables.html', User=User.query.filter_by(password=password, username=username))
	return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
	lives = 3
	if request.method == 'POST':
		form_data = request.form['form_submit']
		find_false = re.search(r"\'obey_humans'\:\sFalse", form_data)
		if find_false:
			return render_template('success.html')
		else:
			lives -= 1
			flash(f'ERROR: Main Systems still functional. You have {lives} more attempts')
			return redirect(url_for('submit'))

	return render_template('submit.html')		


# Drop/Create all Tables
db.drop_all()
db.create_all()
user = User('maeve', 'clementine')
db.session.add(user)
db.session.commit()

if __name__ == '__main__':
	app.run(debug = True)
	

