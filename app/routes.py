#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from flask import render_template
from flask import send_file
from flask import request
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
DEFAULT_INTERVAL = 5
DEFAULT_TYPE = 'increase'
CAMPAIGN_NAME = {'data':'宣誓人', 'peace':'和平精英'}
PEACE_TYPE = "peace"
NORMAL_TYPE = "data"

@app.route('/test')
def test():
	fetch.fetchPeaceData()
	return 'Hello World'

@app.route('/')
@app.route('/index')
def index():
	params = getGraphParam(request, NORMAL_TYPE)
	date = params['date']
	filepath = f'{app.instance_path}/data/{date}.csv'
	title = '超新星宣誓代表+护旗手 ' + date
	return showDataInTable(date, filepath, title, params['interval'])

@app.route('/peace')
def peace():
	params = getGraphParam(request, PEACE_TYPE)
	date = params['date']
	filepath = f'{app.instance_path}/peace/{date}.csv'
	title = '超新星和平精英 ' + date
	return showDataInTable(date, filepath, title, params['interval'])

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
	return render_template("filelist.html", files = filenames, title='2020超新星榜单源数据下载')

@app.route("/rawData/<path:campaign>/<path:filename>")
def downloadRawData(campaign, filename):
    dirpath = os.path.join('.' + app.instance_path, campaign + '/' + filename)
    print(app.instance_path)
    newName = CAMPAIGN_NAME[campaign] + '-' + filename
    return send_file(dirpath, as_attachment=True, attachment_filename=newName)

@app.route('/graph')
def graph():
    params = getGraphParam(request, NORMAL_TYPE)
    date = params['date']
    title = f'超新星宣誓代表+护旗手实时数据图表 {date}'
    filepath = f'{app.instance_path}/data/{date}.csv'
    
    return showDataInGraph(date, filepath, title, params['interval'], params['type'], 'graph.html')

@app.route('/peaceGraph')
def peaceGraph():
    params = getGraphParam(request, PEACE_TYPE)
    date = params['date']
    title = f'超新星和平精英实时数据图表 {date}'
    filepath = f'{app.instance_path}/peace/{date}.csv'

    return showDataInGraph(date, filepath, title, params['interval'], params['type'], 'peaceGraph.html')

def getGraphParam(request, type):
    params = {}
    dateParam = request.args.get('date')
    params['date'] = datetime.now().strftime('%m-%d').strip('\"')
    if dateParam is not None:
        params['date'] = dateParam
    elif type == PEACE_TYPE:
    	params['date'] = '07-22'

    intervalParam = request.args.get('interval')
    params['interval'] = DEFAULT_INTERVAL
    if intervalParam is not None:
        params['interval'] = int(intervalParam)

    typeParam = request.args.get('type')
    params['type'] = DEFAULT_TYPE
    if typeParam is not None:
        params['type'] = typeParam
    return params

def showDataInTable(date, filepath, title, interval):
	if os.path.exists(filepath):
		table = pd.read_csv(filepath)

		# 读取选手
		stars = list(table.columns)[1:11]

		# 读取N分钟前的数据
		previous = table.iloc[-interval:-interval+1,1:11].values.tolist()[0]
		dataList = table.iloc[-1:,1:11].values.tolist()[0]
		increase = []

		for index in range(0,10):
			increase.append(dataList[index] - previous[index])

		data = {'选手':stars, '当前票数':dataList, '涨幅':increase}
		df=pd.DataFrame(data = data)
		return render_template("index.html", data=df.to_html(index=False), title = title)
	else:
		return 'File ' + filepath + ' not exists'

def showDataInGraph(date, filepath, title, interval, type, graphFile):
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
		
		# 开始阅读图表
		index = 1 #这个是行数
		for row in csv_reader:
			if index % interval == 0:
				times.append(row[0])
				for i in range(1, 11):
					if type == 'increase':
						values[i-1].append(int(row[i]) - int(previousCount[i-1]))
						previousCount[i-1] = row[i]
					else:
						values[i-1].append(int(row[i]))
			index = index + 1
		
		values = trimData(values)
		times = trimTime(times)

		return render_template(graphFile, title = title, values=values, labels=times, legends=legends, date = date)


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
