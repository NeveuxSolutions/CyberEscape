from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')