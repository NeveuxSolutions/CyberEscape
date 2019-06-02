from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/begin')
def begin():
	return render_template('begin.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/submit')
def submit():
	return render_template('submit.html')


if __name__ == '__main__':
	app.run(debug=True)