# /app.py
from flask import Flask, render_template, request
import pymongo
from urllib import parse
import math
import random
from datetime import datetime
from datetime import timedelta
import urllib.parse

#Flask 객체 인스턴스 생성!!
app = Flask(__name__)


host = "localhost"
port = "27017"
user = "test_admin"
pwd = "admin"
db = "admin"

client = pymongo.MongoClient(f'mongodb://{user}:{urllib.parse.quote_plus(pwd)}@{host}:{port}/{db}')
db_conn = client.get_database(db)
collection = db_conn.get_collection("youtube")
query1= {"title" : "안녕하세요 보겸입니다"}

    
@app.route('/') # 접속하는 url
def index():
    return render_template('index.html')


@app.route('/bokeyem', methods=['POST']) # 접속하는 url
def bokeyem():
    result=collection.find(query1)
    return render_template('index.html', data=result)

@app.route('/search')
def genre():
    name=request.args.get('radio')
    order=request.args.get('radio2')
    startDate=request.args.get('startDate')
    endDate=request.args.get('endDate')
    genre=request.args.get('genre')
    query2={"categoryId": int(genre)}
    print(type(order))

    if startDate =='' and endDate == '' : #날짜 선택이 안됐을때
        query2={"categoryId": int(genre)}
        result=collection.find(query2)
        if order is None:
            result.sort("view_count",-1)
        else:
            result.sort(order, -1)

    else:           #날짜 선택이 됐을때
        if endDate=='': #시작날짜만 선택됐을때
            startDate=datetime.strptime(startDate, '%Y-%m-%d')
            query2={"publishedAt": {'$gte' : startDate}}
            result = collection.find(query2)
            if order is None:
                result.sort("publishedAt", 1)
            else:
                result.sort(order, -1)
        elif startDate=='': #종료날짜만 선택됐을때
            print("no")
        #둘다 선택됐을때
        else:
            startDate=datetime.strptime(startDate, '%Y-%m-%d')
            endDate=datetime.strptime(endDate, '%Y-%m-%d')
            endDate=endDate.replace(hour=23, minute=59, second=59)
            print(endDate)
            #endDate=startDate+timedelta(days=1)
            query2={"publishedAt": {'$gte' : startDate, '$lte':endDate}}
            result=collection.find(query2)
            if order is None:
                result.sort("publishedAt", 1)
            else:
                result.sort(order, -1)
    print("-------------------------------")
    print()
    print(startDate)
    print(endDate)
    print(genre)
    print()
    print("-------------------------------")
    print(result)

    return render_template('index.html', data=result)
    




if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)