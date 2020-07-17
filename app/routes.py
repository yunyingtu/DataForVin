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

NUM_MAX_POINTS = 90

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
	title = '超新星和平精英 ' + currentDate
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
	title = '超新星宣誓代表+护旗手 ' + date
	if os.path.exists(filepath):
		table = pd.read_csv(filepath)
		return render_template("index.html", data=table.to_html(), title = title)
	else:
		return 'File ' + filepath + ' not exists'

@app.route('/graph')
def graph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	title = '超新星宣誓代表+护旗手实时数据图表 ' + currentDate
	return showDataInGraph(filepath, title)

@app.route('/peaceGraph')
def peaceGraph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/peace/{currentDate}.csv'
	title = '超新星和平精英实时数据图表 ' + currentDate
	return showDataInGraph(filepath, title)

def showDataInGraph(filepath, title):
	with open(filepath, 'r') as f:
		times = []
		values = []
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
		dataObjects = []
		index = 0
		
		values = trimData(values)
		times = trimTime(times)

		return render_template('graph.html', title = title, values=values, labels=times, legends=legends)


def trimData(values):
	trimmedValues = []
	length = len(values[0])
	# 最多显示90个点
	if (length < NUM_MAX_POINTS):
		return values;
	for value in values:
		trimmedValues.append(value[-NUM_MAX_POINTS:])
	return trimmedValues

def trimTime(times):
	if (len(times) < NUM_MAX_POINTS):
		return times
	return times[-NUM_MAX_POINTS:]	
