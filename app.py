from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os
import redis
import time


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

driver = '{ODBC Driver 17 for SQL Server}'
server = 'sqlserver-1002119262-saarthakmudigeregirish.database.windows.net'
database = 'DataBase-1002119262-SaarthakMudigereGirish'
username = 'saarthakmudigeregirish'
password = 'Hello123'

# Establish the connection
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Create a cursor object
cursor = conn.cursor()

# Redis connection details
redis_host = 'Redis-1002119262-SaarthakMudigereGirish.redis.cache.windows.net'
redis_port = 6379
redis_password = 'l2CPHbqqk4w90H19Tmvm0n2ykWFLefcyBAzCaA1MX8M='

# Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
#redis_client.flushall()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page1/", methods=['GET', 'POST'])
def page1():
    query_time = []
    # salpics = []
    time_query = []
    for i in range(30):
        time_query.append(i + 1)

    query = "SELECT id FROM dbo.all_month TABLESAMPLE(1000 ROWS)"
    for i in time_query:
        start = time.time()
        cursor.execute(query)
        end = time.time()
        diff = end - start
        query_time.append(diff)
    '''
    row = cursor.fetchall()
    for i in row:
        salpics.append(i)'''

    return render_template("1)Page.html", time_query=time_query, query_time=query_time)


@app.route("/page2/", methods=['GET', 'POST'])
def page2():
    lat = ""
    long = ""
    query_time = []
    # salpics = []
    time_query = []
    if request.method == "POST":
        lat = request.form['lat']
        long = request.form['long']

        minlat = request.form['minlat']
        maxlat = request.form['maxlat']
        minlong = request.form['minlong']
        maxlong = request.form['maxlong']

        for i in range(30):
            time_query.append(i + 1)

        if lat!='':
            query = "SELECT place FROM dbo.all_month TABLESAMPLE(1000 ROWS) WHERE (6371 * ACOS(COS(RADIANS(?)) * COS(RADIANS(latitude)) * COS(RADIANS(longitude) - RADIANS(?)) + SIN(RADIANS(?)) * SIN(RADIANS(latitude)))) <= 100; "
        else:
            query = f"SELECT * FROM dbo.city WHERE lat BETWEEN ? AND ? AND lon BETWEEN ? AND ?"


        for i in time_query:
            start = time.time()
            if lat!='':
                cursor.execute(query, lat, long, lat)
            else:
                cursor.execute(query, minlat, maxlat, minlong, maxlong)
            end = time.time()
            diff = end - start
            query_time.append(diff)

            '''row = cursor.fetchall()
            for i in row:
                salpics.append(i)'''
    return render_template("2)Page.html", time_query=time_query, query_time=query_time)


@app.route("/page3/", methods=['GET', 'POST'])
def page3():
    time_query = []
    query_time = []
    redis_time = []

    for i in range(30):
        time_query.append(i + 1)

    query = "SELECT id FROM dbo.all_month TABLESAMPLE(1000 ROWS)"
    for i in time_query:
        start = time.time()
        cursor.execute(query)
        end = time.time()
        query_time.append(end-start)

        rows = cursor.fetchall()
        temp_result = ""
        for j in rows:
            temp_result = temp_result + str(j)

        redis_client.set(i, temp_result)
        s = time.time()
        temp = redis_client.get(i)
        e = time.time()
        redis_time.append(e - s)

    return render_template("3)Page.html", query_time=query_time, time_query=time_query, redis_time=redis_time)


@app.route("/page4/", methods=['GET', 'POST'])
def page4():
    time_query = []
    query_time = []
    redis_time = []
    if request.method == "POST":
        lat = request.form['lat']
        long = request.form['long']
        for i in range(30):
            time_query.append(i + 1)

        query = "SELECT place FROM dbo.all_month TABLESAMPLE(1000 ROWS) WHERE (6371 * ACOS(COS(RADIANS(?)) * COS(RADIANS(latitude)) * COS(RADIANS(longitude) - RADIANS(?)) + SIN(RADIANS(?)) * SIN(RADIANS(latitude)))) <= 100; "
        for i in time_query:
            start = time.time()
            cursor.execute(query, lat, long, lat)
            end = time.time()
            query_time.append(end-start)

            rows = cursor.fetchall()
            temp_result = ""
            for j in rows:
                temp_result = temp_result + str(j)

            redis_client.set(i, temp_result)
            s = time.time()
            temp = redis_client.get(i)
            e = time.time()
            redis_time.append(e - s)

    return render_template("4)Page.html", query_time=query_time, time_query=time_query, redis_time=redis_time)


if __name__ == "__main__":
    app.run(debug=True)