#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from flask import render_template
from flask import send_file
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
CAMPAIGN_NAME = {'data':'宣誓人', 'peace':'和平精英'}

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
	title = '超新星宣誓代表+护旗手 ' + currentDate
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

@app.route('/rawData')
def rawData():
	filenames = []
	startDate = 17
	currentDate = int(datetime.now().strftime('%d').strip('\"'))
	for day in range(startDate, currentDate + 1):
		filename = '07-' + str(day) + '.csv'
		filenames.append(filename)
	return render_template("filelist.html", files = filenames)

@app.route("/rawData/<path:campaign>/<path:filename>")
def downloadRawData(campaign, filename):
    dirpath = os.path.join(app.instance_path, campaign + '/' + filename)
    newName = CAMPAIGN_NAME[campaign] + '-' + filename
    return send_file(dirpath, as_attachment=True, attachment_filename=newName)

@app.route('/graph')
def graph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/data/{currentDate}.csv'
	title = '超新星宣誓代表+护旗手实时数据图表 ' + currentDate
	return showDataInGraph(filepath, title, 5)

@app.route('/peaceGraph')
def peaceGraph():
	currentDate = datetime.now().strftime('%m-%d').strip('\"')
	filepath = f'{app.instance_path}/peace/{currentDate}.csv'
	title = '超新星和平精英实时数据图表 ' + currentDate
	return showDataInGraph(filepath, title, 1)

def showDataInGraph(filepath, title, interval):
	with open(filepath, 'r') as f:
		csv_reader = csv.reader(f, delimiter=',')

		# 准备图标所需要的各项数据
		times = []
		values = []
		for i in range(0, 10):
			values.append([])
		legends = next(csv_reader)[1:11]

		# 这个是为间歇存储数据用的。存的是当前数据点之前的一个数据点的真实数字（非涨幅）
		# 初始化到本日数据的第一行数据
		previousCount = next(csv_reader)[1:11]
		
		# 开始阅读图标
		index = 1 #这个是行数
		for row in csv_reader:
			if index % interval == 0:
				times.append(row[0])
				for i in range(1, 11):
					values[i-1].append(int(row[i]) - int(previousCount[i-1]))
					previousCount[i-1] = row[i]
			index = index + 1
		
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
