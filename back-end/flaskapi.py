from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# 连接MySQL数据库
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    database="arduino"
)


# 创建游标对象
mycursor = mydb.cursor()

# 执行查询操作
mycursor.execute("SELECT is_available FROM parking")

# 获取查询结果
result = mycursor.fetchall()

# 将结果存储到Python列表中
is_available_list = [row[0] for row in result]

#将0/1转换为前端使用的字符串
is_available=[''] * 24
for i in range(len(is_available_list)):
    if (is_available_list[i]=='1'):
        is_available[i]='empty'
    elif (is_available_list[i]=='0'):
        is_available[i] = 'occupied'
    else:
        print("error")

#把从数据库中获得的数据存储到一个spots格式的字典中
spots_p = [
        { 'id': 'A1', 'status': is_available[0] },
        { 'id': 'A2', 'status': is_available[1] },
        { 'id': 'A3', 'status': is_available[2] },
        { 'id': 'A4', 'status': is_available[3] },
        { 'id': 'A5', 'status': is_available[4] },
        { 'id': 'A6', 'status': is_available[5] },
        { 'id': 'B1', 'status': is_available[6] },
        { 'id': 'B2', 'status': is_available[7] },
        { 'id': 'B3', 'status': is_available[8] },
        { 'id': 'B4', 'status': is_available[9] },
        { 'id': 'B5', 'status': is_available[10] },
        { 'id': 'B6', 'status': is_available[11] },
        { 'id': 'C1', 'status': is_available[12] },
        { 'id': 'C2', 'status': is_available[13] },
        { 'id': 'C3', 'status': is_available[14] },
        { 'id': 'C4', 'status': is_available[15] },
        { 'id': 'C5', 'status': is_available[16] },
        { 'id': 'C6', 'status': is_available[17] },
        { 'id': 'D1', 'status': is_available[18] },
        { 'id': 'D2', 'status': is_available[19] },
        { 'id': 'D3', 'status': is_available[20] },
        { 'id': 'D4', 'status': is_available[21] },
        { 'id': 'D5', 'status': is_available[22] },
        { 'id': 'D6', 'status': is_available[23] },
    ]

@app.route('/get_spots_status', methods=['GET'])
def get_spots_status():
    spots = spots_p
    return jsonify({'spots': spots})


if __name__ == '__main__':
    app.run()

