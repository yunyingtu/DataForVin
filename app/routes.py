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

@app.route('/test')
def test():
	fetch.fetchPeaceData()
	return 'Hello World'

@app.route('/')
@app.route('/index')
def index():
	dataset = tablib.Dataset()
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	title = '超新星宣誓代表+护旗手' + currentDate
	if os.path.exists(filepath):
		table = pd.read_csv(filepath)
		return render_template("index.html", data=table.to_html(), title = title)
	else:
		return 'File ' + filepath + ' not exists'

@app.route('/peace')
def peace():
	dataset = tablib.Dataset()
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/peace/{currentDate}.csv'
	title = '超新星和平精英' + currentDate
	if os.path.exists(filepath):
		table = pd.read_csv(filepath)
		return render_template("index.html", data=table.to_html(), title = title)
	else:
		return 'File ' + filepath + ' not exists'

@app.route('/<date>')
def showDate(date):
	dataset = tablib.Dataset()
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	title = '超新星宣誓代表+护旗手' + date
	if os.path.exists(filepath):
		table = pd.read_csv(filepath)
		return render_template("index.html", data=table.to_html(), title = title)
	else:
		return 'File ' + filepath + ' not exists'
	# with open(filepath, 'r') as f:
	# 	dataset.csv = f.read()
	# 	data = dataset.html
	# 	return render_template('index.html', data=data, date = date)

@app.route('/graph')
def graph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	title = '超新星宣誓代表+护旗手实时数据图表' + currentDate
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
					values[i-1].append(row[i])
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
		return render_template('graph.html', title = title, values=values, labels=times, legends=legends)

@app.route('/peaceGraph')
def peaceGraph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/peace/{currentDate}.csv'
	title = '超新星和平精英实时数据图表' + currentDate
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
					values[i-1].append(row[i])
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
		return render_template('graph.html', title = title, values=values, labels=times, legends=legends)
	
