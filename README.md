# Overview
这是一个基于Python-Flask的web application
目前用于2020年超新星运动会数据监测

# Instructions
* Download code (assume it's in a directory /DataForVin)
(The following steps are addressed more in detail in the tutorial: https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* $ cd DataForVin/
* $ mkdir instance
* $ cd instance
* $ mkdir data (这是存储宣誓人榜单数据的地方）
* $ mkdir peace （这是存储和平精英榜单数据的地方）
* $ cd ..
* $ python3 -m venv venv
* $ source venv/bin/activate
* $ export FLASK_APP=fetchData.py
* $ flask run
(In the last step you may need to install multiple dependencies. Just run $pip install ... for whatever module needed)

Then open browser and go to 127.0.0.1:5000

# Data
You could see the example data in 07-15.csv. 

If you want to see any data, change 07-15 to current day's date, and put it into DataForVin/instance/data or DataForVin/instance/peace. Corresponding data will show up in the webpage

