from datetime import datetime, timedelta
import random

import serial
import re
import pymysql


# 生成随机车位id
def random_id():
    return random.randint(1, 24)

# 读串口数据
def read_serial():
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data:
            print(data)

# 获取车位的可用状态
def get_available(id):
    select_is_available = f"""SELECT is_available FROM parking WHERE id = {id}"""
    try:
        cursor.execute(select_is_available)
        is_available = cursor.fetchone()[0]
        print(f"{select_is_available} 查询成功: is_available = {is_available}")
        return is_available
    except:
        print(f"{select_is_available} 查询失败")
        return -1


# 车位有车：车位状态改为无车，记录结束时间
def one(id):
    i = 0
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data:
            match = re.search(r'a:(\d+), d:(\d+)', data)
            if match:
                analog_val = int(match.group(1))
                digital_val = int(match.group(2))
                print(f'Analog value: {analog_val}, Digital value: {digital_val}')
                if digital_val == 0:
                    i = i + 1
                    if i == 5:
                        print(f"{id}号车位的车主已经离开")
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("end_time = " + end_time)
                        sql = f"""UPDATE parking SET is_available=0,end_time='{end_time}' WHERE id = {id}"""
                        try:
                            cursor.execute(sql)
                            db.commit()
                            print(f"{id} 写入 end_time = {end_time} 成功")
                        except:
                            db.rollback()
                            print(f"{id} 写入 end_time = {end_time} 失败")
                        break
    try:
        sql = f"""SELECT start_time, end_time ,total_time FROM parking WHERE id = {id}"""
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("查询失败: 没有找到匹配的数据")
        else:
            start_time = row[0]
            end_time = row[1]
            total_time = row[2]
            hours, remainder = divmod(total_time, 60)
            minutes = remainder
            print(f"开始时间: {start_time}\n结束时间: {end_time}\n总时间:{hours} 小时 {minutes} 分钟\n")
    except Exception as e:
        print(str(e))
        print("查询失败: " + sql)
    return


# 车位无车：车位状态改为有车，记录开始时间
def zero(id):
    i = 0
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data:
            match = re.search(r'a:(\d+), d:(\d+)', data)
            if match:
                analog_val = int(match.group(1))
                digital_val = int(match.group(2))
                print(f'Analog value: {analog_val}, Digital value: {digital_val}')
                if digital_val == 1:
                    i = i + 1
                    if i == 5:
                        print(f"{id}号车位的车主已经到达")
                        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ser.write("start".encode())  # 显示屏开始计时
                        print("start_time = " + start_time)
                        # 写入start_time之前要清空end_time和total_time
                        clean_sql = f"""UPDATE parking SET end_time=NULL,total_time=NULL WHERE id = {id}"""
                        insert_start_time_sql = f"""UPDATE parking SET is_available=1,start_time='{start_time}' WHERE id = {id}"""
                        try:
                            cursor.execute(clean_sql)
                            cursor.execute(insert_start_time_sql)
                            db.commit()
                            print(f"{id} 写入 start_time = {start_time} 成功")
                        except:
                            db.rollback()
                            print(f"{id} 写入 start_time = {start_time} 失败")
                            print("回滚成功")
                        break
    try:
        sql = f"""SELECT start_time FROM parking WHERE id = {id}"""
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("查询失败: 没有找到匹配的数据")
        else:
            print(row)
            print(f"start_time = {row[0]}")
    except Exception as e:
        print(str(e))
        print("查询失败: " + sql)
    return


if __name__ == '__main__':
    try:
        # 打开数据库连接
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='arduino', )
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        ser = serial.Serial('COM5', 9600, timeout=0.5)
        analog_val = 0
        digital_val = 0

        while True:
            print("---" * 20)
            id = random_id()  # 车位id
            is_available = get_available(id)  # 车位是否有车
            if is_available == 1:
                print(f'{id}号车位有车')
                one(id)
            else:
                print("---" * 20)
                print(f'{id}号车位无车')
                zero(id)

    except Exception as e:
        print(str(e))
    finally:
        db.close()
        ser.close()
