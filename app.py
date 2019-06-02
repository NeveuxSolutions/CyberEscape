from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SECRET_KEY'] = "g5ac358c-f0bf-11e5-9e39-d3b532c10a28"
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

		# Create user cookie
		session['username'] = username
		session['password'] = password
		session['admin'] = False
		return render_template('tables.html', User=User.query.filter_by(password=password, username=username))
	return render_template('login.html')

# Drop/Create all Tables
db.drop_all()
db.create_all()
user = User('maeve', 'clementine')
db.session.add(user)
db.session.commit()

if __name__ == '__main__':
	app.run(debug = True)
	

