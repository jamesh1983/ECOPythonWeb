# -*- coding: utf-8 -*-
# filename: main.py
import web
import threading
#import time
import tkinter as tk
from handle import Handle
from datetime import datetime
from threading import Timer
import UIModule
from UIModule import userinterface
#from mbtcpmodule import MBTCP
import pymysql
import mysql
import weixin

urls = (
    '/wx', 'Handle',
)

#class MySQLThread (threading.Thread):
#    def __init__(self, threadID):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#    def run(self):
#        print ("开始线程：" + self.threadID)
#        MySQL.Execute()
#        print ("退出线程：" + self.threadID)

class UIThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        print ("开始线程：" + self.threadID)
        # 创建UI
        UIModule.ui_create()
        #root.mainloop()
        print ("退出线程：" + self.threadID)

def TimeCounter_60():
    # 打印时间函数
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
    mysql.run_mysql()
    mysql.run_mysql_HL()
    #weixin.run_weixin()
    #weixin.repeat_weixin(1440)
    global t1
    t1 = Timer(60, TimeCounter_60)
    t1.start()

#def TimeCounter_600():
    # 打印时间函数
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
#    weixin.repeat_weixin(240)
#    global t2
#    t2 = Timer(600, TimeCounter_600)
#    t2.start()

#def ModBusCommunication(inc):
    #具体触发内容
#    MBTCP.client()

#    global MBTimer
#    MBTimer = Timer(inc, ModBusCommunication, (inc,))
#    MBTimer.start()

#mysql = MySQLThread("mysqlthread")

#def insert_user(userID, weixinID):
# 打开数据库连接
    #try:
        #db = pymysql.connect("rm-uf608104z06w867v86o.mysql.rds.aliyuncs.com", "admin_user", "Abc123xyz", "prodict_database")
# 使用cursor()方法获取操作游标 
        #cursor = db.cursor()
# 使用execute方法执行SQL语句 replace into table( col1, col2, col3 ) values ( val1, val2, val3 )
        #sqlcmd = "INSERT INTO table_user(user_ID, weixinID) VALUES(" + userID + ", '" + weixinID + "')"
        #result = cursor.execute(sqlcmd)
        #db.commit()
# 关闭数据库连接
        #db.close()
        #print (result)
        #return "success"
    #except Exception as Argment:
        #print (Argment)
        #db.rollback()
        #return "fault"

if __name__ == '__main__':
   # X秒打印一次时间
    TimeCounter_60()
    weixin.conn_weixin()
#    TimeCounter_600()
   # X秒与Modbus主机通讯一次
    #ModBusCommunication(10)
   # 初始化对话框
    #ui = UIThread("UIThread")
    #ui.start()
    #mysql.start()
   # 启动web服务
    app = web.application(urls, globals())
    app.run()

