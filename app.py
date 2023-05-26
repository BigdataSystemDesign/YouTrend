# /app.py
from flask import Flask, render_template, request
import pymongo
from urllib import parse
import math
import random
from datetime import datetime
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

    name=request.args.get('radio')
    order=request.args.get('radio2')
    date=request.args.get('date')

    print("-------------------------------")
    print()
    print(date,name,order)
    print()
    print("-------------------------------")
    if order=="video":
        return render_template('hi.html')
    if order=="channel":
        return render_template('hi2.html')

@app.route('/bokeyem', methods=['POST']) # 접속하는 url
def bokeyem():
    result=collection.find(query1)
    return render_template('form.html', data=result)




if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)