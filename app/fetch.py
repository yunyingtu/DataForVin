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
peaceCurrentData = {}

def fetchPeaceData():
    global peaceCurrentData
    headers = {
    'authority': 'matchweb.sports.qq.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://sports.qq.com/mkbsapp/game-for-peace.htm',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': 'pgv_pvid=7576678788; pgv_pvi=1649242112; RK=XpZVzyKsm5; ptcz=d51f3f6b13c8b3af8ac029f108e2af87b8eda4ccbf47999bba9c0caada5ab86a; tvfe_boss_uuid=f3c869278730c337; o_cookie=3346692292; pac_uid=1_3346692292; pgv_si=s7453512704; pgv_info=ssid=s583860268; bossv2_isvip=-1; ts_refer=www.5xzb.com/; ts_uid=3145090918',
    }

    params = (
        ('questionId', ''),
        ('callback', 'jsonp_1594961883604_30859'),
    )

    response = requests.get('https://matchweb.sports.qq.com/html/superNova2020PEL?questionId=&callback=jsonp_1594961883604_30859', headers=headers)
    data = json.loads(response.text[26:-1])

    rawData = data['data']['rank']['heat']

    participants = {}
    for i in rawData:
        participants[i['name']] = int(i['voteNum'])

    currentTime = datetime.now().strftime('%H:%M:%S').strip('\"')
    currentDate = datetime.now().strftime('%m-%d').strip('\"')
    filepath = f'{app.instance_path}/peace/{currentDate}.csv'
    names = []

    if os.path.exists(filepath):
        with open(filepath, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            headers = next(csv_reader)
            names = headers[1:11]
            if len(peaceCurrentData) == 0:
                for row in reversed(list(csv.reader(csv_file))):
                    for i in range(1, 11):
                        peaceCurrentData[headers[i]] = int(row[i])
                    break
    else:
        with open(filepath, mode='w') as myfile:
            writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            allParticipants = sorted(participants.items(), key=operator.itemgetter(1), reverse = True)[:10]
            headers = ['Time']
            for i in allParticipants:
                headers.append(i[0])
            for i in allParticipants:
                headers.append(i[0] + '涨幅')
            writer.writerow(headers)
            names = headers[1:11]

    with open(filepath, mode='a') as myfile:
        writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newdata = [currentTime]
        newDict = {}
        for name in names:
            newdata.append(participants[name])
            newDict[name] = participants[name]
        if len(peaceCurrentData) != 0:
            for name in names:
                newdata.append(participants[name] - peaceCurrentData[name])
            for name in names:
                newdata.append(0)
        writer.writerow(newdata)
        print(newdata)
        peaceCurrentData = newDict


def fetchVoteData():
    global dataDict
    headers = {
        'authority': 'access.video.qq.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'origin': 'https://m.v.qq.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.v.qq.com/activity/h5/super_star/index.html?ovscroll=0&iOSUseWKWebView=1&autoplay=1&actityId=107848&actor_id=&hidetitlebar=1&pg_from=phone_out_mainlist&style=contentbkcolor%3D%23FF5A72&vid=&star_pic=https%253A%252F%252Fpuui.qpic.cn%252Fvupload%252F0%252F1594794205378_0skrcucyxvd.png%252F0&star_name=R1SE_%25E5%2591%25A8%25E9%259C%2587%25E5%258D%2597&isDarkMode=0&uiType=REGULAR&url_from=share&second_share=0&share_from=wxf&from=groupmessage',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cookie': 'pgv_pvid=7576678788; pgv_pvi=1649242112; video_platform=2; RK=XpZVzyKsm5; ptcz=d51f3f6b13c8b3af8ac029f108e2af87b8eda4ccbf47999bba9c0caada5ab86a; tvfe_boss_uuid=f3c869278730c337; video_guid=c93a1aa44a522428; o_cookie=3346692292; pac_uid=1_3346692292; pgv_si=s7453512704; pgv_info=ssid=s583860268; appid=wxa75efa648b60994b; _video_qq_appid=wxa75efa648b60994b; main_login=wx; _video_qq_main_login=wx; openid=oXw7q0KrJh5qJPJ6SUQt4mD_BSL8; _video_qq_openid=oXw7q0KrJh5qJPJ6SUQt4mD_BSL8; refresh_token=34_yY25tzJilCp3iN_NkjpJRtjbQMWbl1aZDQqJ-bglhtonI4oepRt829dEhYg5Prm6u5398NiKR3xR4r7RbZ6HVJjuBEyYRKOKLPED6n498j8; _video_qq_refresh_token=34_yY25tzJilCp3iN_NkjpJRtjbQMWbl1aZDQqJ-bglhtonI4oepRt829dEhYg5Prm6u5398NiKR3xR4r7RbZ6HVJjuBEyYRKOKLPED6n498j8; vuserid=911557870; _video_qq_vuserid=911557870; _video_qq_version=1.1; login_time_last=2020-7-6 12:3:42; access_token=35_qxpcDMtLEbrxB9hhhwOSp3iLQfEIP64MTDlwQo49sWUXgebuSJci72a5R0YJFa8Qfn_FIar80YYpg6Iuws4xZQ; vusession=AxosBydNejcAtPe-oGLZYA..; login_time_init=1594901310; next_refresh_time=6600; _video_qq_access_token=35_qxpcDMtLEbrxB9hhhwOSp3iLQfEIP64MTDlwQo49sWUXgebuSJci72a5R0YJFa8Qfn_FIar80YYpg6Iuws4xZQ; _video_qq_vusession=AxosBydNejcAtPe-oGLZYA..; _video_qq_login_time_init=1594901310; _video_qq_next_refresh_time=6600',
    }

    params = (
        ('raw', '1'),
        ('vappid', '51902973'),
        ('vsecret', '14816bd3d3bb7c03d6fd123b47541a77d0c7ff859fb85f21'),
        ('actityId', '107848'),
        ('pageSize', '200'),
        ('vplatform', '3'),
        ('listFlag', '1'),
        ('pageContext', ''),
        ('extInfo', 'rt=1'),
        ('ver', '1'),
        ('_t', '1594901318665'),
        ('_', '1594901318666'),
    )

    response = requests.get('https://access.video.qq.com/fcgi/getVoteActityRankList', headers=headers, params=params)

    data = json.loads(response.text)
    male = data['data']['mapList']['676734756']

    stars = {}

    for i in male:
        showCount = i['rankInfo']['showVoteCnt']
        voteNum = 0
        if showCount.endswith('万'):
            showCount = showCount[0:-1]
            voteNum = float(showCount) * 10000
        else:
            voteNum = float(showCount)
        stars[i['itemInfo']['name']] = int(voteNum)

    # allStars = sorted(stars.items(), key=operator.itemgetter(1), reverse = True)[:10]
    # sortedStars = collections.OrderedDict(allStars)
    currentTime = datetime.now().strftime('%H:%M:%S').strip('\"')
    currentDate = datetime.now().strftime('%m-%d').strip('\"')
    filepath = f'{app.instance_path}/data/{currentDate}.csv'
    names = []

    if os.path.exists(filepath):
        print('Writing csv.........')
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
            print(allStars)
            headers = ['Time']
            for i in allStars:
                headers.append(i[0])
            for i in allStars:
                headers.append(i[0] + '涨幅')
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
            for name in names:
                newdata.append(0)
        writer.writerow(newdata)
        print(newdata)
        dataDict = newDict
