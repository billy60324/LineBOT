# -*- coding: UTF-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from flask_sslify import SSLify

import os
import random
import MySQLdb

#爬蟲
import requests
from bs4 import BeautifulSoup
import urllib
#from urllib.request import urlretrieve
import re


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#解決UnicodeEncodeError: 'ascii' codec can't encode characters in position 16-17: ordinal not in range(128)

app = Flask(__name__)
sslify = SSLify(app)

# Channel Access Token
line_bot_api = LineBotApi('IvP19kRz9Zu4Kr0Y/3pGz2Vuc02JjWN1I4fS/1xnFebLos+AVVj05VTfL5CaAs+NfzAOVaYMJq1RmGxNSIBau7Xdi5vZRtkL41noO2xZ6zT/ZJxlwoIRWn5nXiHRXqvb3TBr39iVMtsiX7tMw9Z78gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bf73af9b5870cece6813088658ef6545')

def star(token):
    if '牡羊' in token: return 0
    elif '金牛' in token : return 1
    elif '雙子' in token : return 2
    elif '巨蟹' in token : return 3
    elif '獅子' in token : return 4
    elif '處女' in token : return 5
    elif '天秤' in token : return 6
    elif '天蠍' in token : return 7
    elif '射手' in token : return 8
    elif '魔羯' in token : return 9
    elif '水瓶' in token : return 10
    elif '雙魚' in token : return 11
    else : return 12

def DBconnect():
    HOST="billy60324.mysql.pythonanywhere-services.com"
    USER="billy60324"
    PASS="aaa123123"
    DBNAME="billy60324$linebot"
    PORT="3306"

    try:
        db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

        # 執行SQL statement
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")

        # 撈取多筆資料
        results = cursor.fetchall()

        # 迴圈撈取資料
        for record in results:
            col0 = record[0]


        # 關閉連線
        db.close()
    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])

# listen /callback   Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    #app.logger.info( line_bot_api.get_profile(event.source.user_id).display_name )
    #app.logger.info( event.source.user_id + ' : ' + event.message.text.encode('utf-8'))
    app.logger.info( event.source.user_id )
    app.logger.info( ':' )
    app.logger.info( event.message.text.encode('utf-8') )
    #app.logger.info( event.source.user_id )
    #message = TextSendMessage(text=(event.message.text))
    #profile = line_bot_api.get_profile(event.source.user_id)
    #message = TextSendMessage(text=(profile.display_name + ':' + event.message.text))

    HOST="billy60324.mysql.pythonanywhere-services.com"
    USER="billy60324"
    PASS="aaa123123"
    DBNAME="billy60324$linebot"
    PORT="3306"

    #line_bot_api.push_message('U198aeb35f2d801abafa39f6faf3c05eb', TextSendMessage(text=(event.message.text)))
    # shooting ID : U8415848cb28920a4c7dbc849362952e3
    '''
    if event.source.user_id == 'U8415848cb28920a4c7dbc849362952e3':
        line_bot_api.push_message('U198aeb35f2d801abafa39f6faf3c05eb', TextSendMessage(text=(event.message.text)))
        return
    elif event.source.user_id == 'U198aeb35f2d801abafa39f6faf3c05eb':
        line_bot_api.push_message('U8415848cb28920a4c7dbc849362952e3', TextSendMessage(text=(event.message.text)))
        return
    '''
    token = event.message.text.encode('utf-8').split()
    #message = TextSendMessage(text=('null'));
    message = None

    if token[0] == '學習':
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

            # 執行SQL statement
            cursor = db.cursor()

            if len(token) == 3:
                cursor.execute('SELECT ANSWER FROM QA WHERE QUESTION=\'' + token[1] + '\'')
                results = cursor.fetchall()
                if len(results) == 0:
                    cursor.execute('INSERT INTO QA VALUES (\'' + token[1] + '\',\'' + token[2] + '\');')
                    db.commit()
                    message = TextSendMessage(text=('學習成功!'))
                else:
                    message = TextSendMessage(text=('我早就學會了!'))
            else:
                message = TextSendMessage(text=('學習格式錯誤!'))

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])
    elif token[0] == '忘記':
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

            # 執行SQL statement
            cursor = db.cursor()

            if len(token) == 2:
                cursor.execute('SELECT ANSWER FROM QA WHERE QUESTION=\'' + token[1] + '\'')
                results = cursor.fetchall()
                if len(results) != 0:
                    cursor.execute('DELETE FROM QA WHERE QUESTION=\'' + token[1] + '\'')
                    db.commit()
                    message = TextSendMessage(text=('好啦!人家忘記了嘛!'))
                else:
                    message = TextSendMessage(text=('你壞壞!人家根本沒學過那個!'))
            else:
                message = TextSendMessage(text=('忘記格式錯誤!'))

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])
    elif token[0] == '天氣':
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=1675151&APPID=2bd13257e4836cacee8320ba8fac2334&units=metric') #新竹&lang=zh_tw
        r.encoding = 'utf-8'
        message = TextSendMessage(text=( r.json()['city']['name'].encode('ascii', 'ignore') + ' ' + str(r.json()['list'][0]['main']['temp']).encode('ascii', 'ignore') + ' ' +r.json()['list'][0]['weather'][0]['description'] ).encode('ascii', 'ignore') )
    elif token[0] == '照片':
        message = ImageSendMessage(original_content_url='http://i.imgur.com/OaWqtHC.gif', preview_image_url='http://i.imgur.com/OaWqtHC.gif')
    elif '處男' in token[0]:
        message = ImageSendMessage(original_content_url='https://i.imgur.com/80XdHuM.jpg', preview_image_url='https://i.imgur.com/80XdHuM.jpg')
    elif token[0] == '星座':
        if len(token) == 2 and star(token[1]) != 12:
            message = TextSendMessage(text=('http://astro.click108.com.tw/daily_0.php?iAstro=' + str( star(token[1]) )))
        else:
            message = TextSendMessage(text=('你應該是天馬座吧?'))
    elif token[0] == '抽':
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

            # 執行SQL statement
            cursor = db.cursor()
            cursor.execute('SELECT URL FROM IMGUR_GRAPH')
            results = cursor.fetchall()

            # 迴圈撈取資料
            picture = []
            for record in results:
                picture.append(record[0])

            output = picture[random.randint(0,99999)%len(picture)]
            #只支援https
            if output[4] != 's':
                output = output.replace('http','https')
            message = ImageSendMessage(original_content_url=output, preview_image_url=output)

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])
    elif token[0] == '抽抽':
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')
            cursor = db.cursor()
            if len(token) == 2:
                if ((token[1].startswith('http://') or token[1].startswith('https://')) and token[1].endswith('jpg')):
                    cursor.execute('INSERT INTO USER_GRAPH VALUES (\'' + token[1] + '\');')
                    db.commit()
                    message = TextSendMessage(text=('完工拉!'))
                else:
                    message = TextSendMessage(text=('是不是放錯圖片連結了R'))
            else:
                # 執行SQL statement
                cursor.execute('SELECT URL FROM USER_GRAPH')
                results = cursor.fetchall()

                # 迴圈撈取資料
                picture = []
                for record in results:
                    picture.append(record[0])

                output = picture[random.randint(0,99999)%len(picture)]
                #只支援https
                if output[4] != 's':
                    output = output.replace('http','https')
                message = ImageSendMessage(original_content_url=output, preview_image_url=output)

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])
    elif '吃什麼' in token[0] or '吃啥' in token[0]:
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

            # 執行SQL statement
            cursor = db.cursor()
            cursor.execute('SELECT RESTAURANT FROM MEAL')
            results = cursor.fetchall()

            # 迴圈撈取資料
            restaurant = []
            for record in results:
                restaurant.append(record[0])


            message = TextSendMessage(text=(restaurant[random.randint(0,999)%len(restaurant)]))

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])
    elif token[0] == '選' and len(token) >= 4 and token[1] == '(' and token[len(token)-1] == ')':
        message = TextSendMessage(text=(token[random.randint(0,999)%(len(token)-3)+2]))
    elif '要不要' in token[0]:
        if random.randint(0,999)%2:
            message = TextSendMessage(text=('要'))
        else:
            message = TextSendMessage(text=('不要'))
    elif '會不會' in token[0]:
        if random.randint(0,999)%2:
            message = TextSendMessage(text=('會'))
        else:
            message = TextSendMessage(text=('不會'))
    elif '484' in token[0]:
        if random.randint(0,999)%2:
            message = TextSendMessage(text=('4'))
        else:
            message = TextSendMessage(text=('84'))
    elif '是不是' in token[0]:
        if random.randint(0,999)%2:
            message = TextSendMessage(text=('是'))
        else:
            message = TextSendMessage(text=('不是'))
    elif '有沒有' in token[0]:
        if random.randint(0,999)%2:
            message = TextSendMessage(text=('有'))
        else:
            message = TextSendMessage(text=('沒有'))
    else:
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')

            # 執行SQL statement
            cursor = db.cursor()

            cursor.execute('SELECT ANSWER FROM QA WHERE QUESTION=\'' + token[0] + '\'')

            # 撈取多筆資料
            results = cursor.fetchall()

            # 迴圈撈取資料
            for record in results:
                col0 = record[0]
                message = TextSendMessage(text=(col0))

                #print event.reply_token
                #line_bot_api.reply_message(event.reply_token,  message)

            # 關閉連線
            db.close()
        except MySQLdb.Error as e:
            app.logger.info('Error ' + str(e.args[0]) + ':' + e.args[1])



    #如果message不是None才處理
    if message:
        if message.type == 'text':
            app.logger.info( 'LineBOT reply : ' + message.text )
        elif message.type == 'image':
            app.logger.info( 'LineBOT reply image: ' + message.original_content_url )
        line_bot_api.reply_message(event.reply_token,  message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
