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
		legends = []
		colors = ["rgba(176,224,230,1)", "rgba(12,28,56,1)", "rgba(132,175,212,1)", "rgba(203,167,249,1)", 
		"rgba(255,157,162,1)", "rgba(148, 7, 34,1)", "rgba(95,75,139,1)", "rgba(98,3,23,1)", "rgba(11,39,25,1)", "rgba(255,45,81,1)"]
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
		dataObjects = []
		index = 0
		for value in values:
			obj = {}
			obj['label'] = legends[index]
			obj['fill'] = False
			obj['borderColor'] = colors[index]
			obj['backgroundColor'] = colors[index]
			obj['data'] = value
			index = index+1
			dataObjects.append(obj)
			print(dataObjects)
		return render_template('graph.html', values=values, labels=times, legends=legends)
	
