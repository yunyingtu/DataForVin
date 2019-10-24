#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

import requests
import json
import operator
import csv
import collections
import os
from datetime import datetime
from app import app

dataDict = {}

def fetchVoteData():
    global dataDict
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://sports.qq.com/mkbsapp/yuanqi.htm?shareKey=2402de2a6d7d23a19d9dcaaae34b97b9&ptag=4_7.6.0.22280_wxf&dt_dapp=1&from=groupmessage&isappinstalled=0&ptag=4_7.6.0.22280_sina',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('questionId', ''),
    )

    response = requests.get('https://matchweb.sports.qq.com/html/superNovaInfo2?questionId=', headers=headers)
    data = json.loads(response.text)
    male = data['data']['rank']['male']
    female = data['data']['rank']['female']

    stars = {}

    for i in male:
    	stars[i['name']] = int(i['voteNum'])

    for i in female:
    	stars[i['name']] = int(i['voteNum'])

    # allStars = sorted(stars.items(), key=operator.itemgetter(1), reverse = True)[:10]
    # sortedStars = collections.OrderedDict(allStars)
    currentTime = datetime.now().strftime('%H:%M:%S').strip('\"')
    currentDate = datetime.now().strftime('%m-%d').strip('\"')
    filepath = f'{app.instance_path}/data/{currentDate}.csv'
    names = []

    if os.path.exists(filepath):
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            headers = next(csv_reader)
            names = headers[1:11]
            if len(dataDict) == 0:
                for row in reversed(list(csv.reader(csv_file))):
                    for i in range(1, 11):
                        dataDict[headers[i]] = int(row[i])
                    break
    else:
        with open(filepath, mode='w') as myfile:
            writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            allStars = sorted(stars.items(), key=operator.itemgetter(1), reverse = True)[:10]
            headers = ['Time']
            for i in allStars:
                headers.append(i[0])
            writer.writerow(headers)
            names = headers[1:11]

    with open(filepath, mode='a') as myfile:
        writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newdata = [currentTime]
        newDict = {}
        for name in names:
            newdata.append(stars[name])
            newDict[name] = stars[name]
        if len(dataDict) != 0:
            for name in names:
                newdata.append(stars[name] - dataDict[name])
        writer.writerow(newdata)
        print(newdata)
        dataDict = newDict
