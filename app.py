# /app.py
from flask import Flask, render_template, request
import pymongo
from urllib import parse
import math
import random
from datetime import datetime
from datetime import timedelta
import urllib.parse
from bson.son import SON

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
categories = [
    ("영화 & 애니메이션"), #0~1
    ("영화 & 애니메이션"),
    ("자동차 & 차량"), #2~9
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("자동차 & 차량"),
    ("음악"), #10~14
    ("음악"), 
    ("음악"),
    ("음악"),
    ("음악"),
    ("애완동물 & 동물"), #15~16
    ("애완동물 & 동물"),
    ("스포츠"), #17
    ("짧은 영화"), #18
    ("여행 & 이벤트"), #19
    ("게임"), #20
    ("비디오블로그"), #21
    ("사람 & 블로그"), #22
    ("코미디"), #23
    ("엔터테이먼트"), #24
    ("뉴스 & 정치학"), #25
    ("스타일"), #26
    ("교육"), #27
    ("과학&기술"), #28~29
    ("과학&기술"),
    ("영화"), #30
    ("애니매이션"), #31
    ("액션"), #32
    ("클래식"), #33
    ("코미디"), #34
    ("다큐멘터리"), #35
    ("드라마"), #36
    ("가족"), #37
    ("외국어"), #38
    ("공포"), #39
    ("공상과학"), #40
    ("스릴러"), #41
    ("스포츠"), #42
    ("쇼"), #43
    ("예고편") #44
]

print(categories[3])
    
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
    resultForm=request.args.get('radio2')
    print(resultForm)
    print(type(resultForm))
    startDate=request.args.get('startDate')
    endDate=request.args.get('endDate')
    genre=int(request.args.get('genre'))
    radio=request.args.get('radio')
    query2={"categoryId": int(genre)}
    result=None


    if radio=="genre_button":
        if resultForm=="channel":
            query2=[
            {
                '$match':{
                    'categoryId': int(genre)
                }
            },
            {
                '$group': {
                '_id': '$channelTitle',
                'totalViews': {'$sum': '$view_count'},
            }
            },
            {
                '$sort':{
                    'totalViews':-1
                }
            }

        ]
            resultForm='channel'
            result=collection.aggregate(query2)
        
        elif resultForm=="video" or resultForm is None:
            query2={"categoryId": genre}
            result=collection.find(query2).sort("view_count",-1)

    elif radio=="date_button":
        if endDate=='': #시작날짜만 선택됐을때
            startDate=datetime.strptime(startDate, '%Y-%m-%d')
            query2={"publishedAt": {'$gte' : startDate}}
            result=collection.find(query2)
        elif startDate=='': #종료날짜만 선택됐을때
            print("no")
        #둘다 선택됐을때
        else:
            startDate=datetime.strptime(startDate, '%Y-%m-%d')
            endDate=datetime.strptime(endDate, '%Y-%m-%d')
            endDate=endDate.replace(hour=23, minute=59, second=59)
            print(endDate)
            query2={"publishedAt": {'$gte' : startDate, '$lte':endDate}}
            result=collection.find(query2).sort("publishedAt",1)



        if resultForm=='video' or resultForm is None:
            resultForm="video"
        elif resultForm=='channel':
            query2=[
            {
                '$match':{
                    'publishedAt' : {'$gte' : startDate, '$lte': endDate}
                }
            },
            {
                '$group': {
                '_id': '$channelTitle',
                'totalViews': {'$sum': '$view_count'},
            }
            },
            {
                '$sort':{
                    'totalViews':-1
                }
            }

        ]
            result=collection.aggregate(query2)
            resultForm="channel"
        
        elif resultForm=='genre':
             query2=[
            {
                '$group': {
                '_id': '$categoryId',
                'totalViews': {'$sum': '$view_count'},
            }
            },
            {
                '$sort':{
                    'totalViews':-1
                }
            }

        ]
             result=collection.aggregate(query2)
             resultForm="genre"
            



    return render_template('index.html', data=result, resultForm=resultForm, categories=categories)


    # elif radio=="date_button":
    

    # if startDate =='' and endDate == '' : #날짜 선택이 안됐을때
    #     query2={"categoryId": int(genre)}
    #     result=collection.find(query2).sort("view_count",-1)
    # else:           #날짜 선택이 됐을때
    #     if endDate=='': #시작날짜만 선택됐을때
    #         startDate=datetime.strptime(startDate, '%Y-%m-%d')
    #         query2={"publishedAt": {'$gte' : startDate}}
    #     elif startDate=='': #종료날짜만 선택됐을때
    #         print("no")
    #     #둘다 선택됐을때
    #     else:
    #         startDate=datetime.strptime(startDate, '%Y-%m-%d')
    #         endDate=datetime.strptime(endDate, '%Y-%m-%d')
    #         endDate=endDate.replace(hour=23, minute=59, second=59)
    #         print(endDate)
    #         query2={"publishedAt": {'$gte' : startDate, '$lte':endDate}}
    #         result=collection.find(query2).sort("publishedAt",1)

    # if resultForm=='' or resultForm=='video':     #결과 형태가 video일때
    #     resultForm='video'
    #     print("hello")
    # elif resultForm=='channel':                   #결과 형태가 channel일때
    #     query2=[
    #         {
    #             '$match':{
    #                 'categoryId': int(genre)
    #             }
    #         },
    #         {
    #             '$group': {
    #             '_id': '$channelTitle',
    #             'totalViews': {'$sum': '$view_count'},
    #         }
    #         },
    #         {
    #             '$sort':{
    #                 'totalViews':-1
    #             }
    #         }

    #     ]
    #     resultForm='channel'
    #     result=collection.aggregate(query2)
    
    #elif resultForm==''        

    # print("-------------------------------")
    # print()
    # print(startDate)
    # print(endDate)
    # print(genre)
    # print()
    # print(resultForm)
    # print("-------------------------------")
    # print(result)

    
    




if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)