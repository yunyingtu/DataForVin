#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from flask import render_template
from app import app
from app import fetch
from datetime import datetime
import os
import csv
import tablib
import pandas as pd
import numpy as np
import plotly.graph_objs as go

@app.route('/')
@app.route('/index')
def index():
	dataset = tablib.Dataset()
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	with open(filepath, 'r') as f:
		dataset.csv = f.read()
		data = dataset.html
		return render_template('index.html', data=data, date = currentDate)

@app.route('/<date>')
def showDate(date):
	dataset = tablib.Dataset()
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	with open(filepath, 'r') as f:
		dataset.csv = f.read()
		data = dataset.html
		return render_template('index.html', data=data, date = date)

@app.route('/graph')
def graph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	with open(filepath, 'r') as f:
		times = []
		values = []
		hll = []
		legends = []
		csv_reader = csv.reader(f, delimiter=',')
		count = 0
		star = 1
		for i in range(0, 10):
			values.append([])
		for row in csv_reader:
			if count != 0:
				times.append(row[0])
				for i in range(1, 11):
					values[i-1].append(row[i+10])
			else:
				legends = row[1:11]
			count = count + 1
		return render_template('graph.html', values=values, labels=times, legends=legends)
	
