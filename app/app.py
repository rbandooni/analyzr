from flask import Flask, render_template,request,redirect,url_for
from tweets import QueryTwitter
import pandas as pd
import json
import os
from os import path

app = Flask(__name__)

extra_dirs = ['/user/ubuntu/cs6030-project/templates',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
	for dirname, dirs, files in os.walk(extra_dir):
		for filename in files:
			filename = path.join(dirname,filename)
			if path.isfile(filename):
				extra_files.append(filename)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == "GET":
		return render_template('default.html')
	else:
		return "Error: Only GET requests are allowed for this route"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

	redirectMessage = 'Please enter a search term'
	if request.method == 'GET':
		return redirect(url_for('index'), code=302)
	else:
		searchParam = request.form['keyword']
		(a,b,c,d,e) = QueryTwitter(searchParam)
		return render_template('dashboard.html', doughnut=json.dumps(a),mapPlot=b,sources_plot=json.dumps(c),sentiment_pie=json.dumps(d),table=json.dumps(e),keyword=searchParam)

@app.route('/report', methods=['GET', 'POST'])
def chat():
	return render_template('report.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
	return render_template('image.html')

@app.route('/about', methods=['GET'])
def about():
	if request.method == 'GET':
		return render_template('about.html')
	else:
		return "Only GET request are allowed for this route"

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == "__main__":
	# app.run(extra_files=extra_files)
	app.run(host='0.0.0.0')
