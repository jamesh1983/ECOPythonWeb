import web
import threading
import time
import tkinter as tk
import pymysql
import settings
import model
#import mysql
from datetime import datetime
from threading import Timer
from web import form
#from UIModule import userinterface
#from mbtcpmodule import MBTCP
#from web.contrib.template import render_jinja
loginuser=''
web.config.debug = True
app = web.application(settings.urls, globals())
render = web.template.render('templates')
idlistdata = model.CurrentData.getColumnList('id')
namelistdata = model.CurrentData.getColumnList('Name')
poplistdata = model.CurrentData.getColumnList('Population')
#render = render_jinja(
#    'templates',
#    encoding = 'utf-8',
#)
#class MySQLThread (threading.Thread):
#    def __init__(self, threadID):
#        threading.Thread.__init__(self)
#        self.threadID = threadID
#    def run(self):
#        print ("开始线程：" + self.threadID)
#        MySQL.Execute()
#        print ("退出线程：" + self.threadID)
def TimeCounter_5():
    # 打印时间函数
    print('T1现在时间：',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
    #mysql.run_mysql()
    #weixin.run_weixin()
    #weixin.repeat_weixin(1440)
    global t1
    t1 = Timer(5, TimeCounter_5)
    t1.start()
def TimeCounter_10():
    # 打印时间函数
    print('T2现在时间：',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
    #weixin.repeat_weixin(9)
    global t2
    t2 = Timer(10, TimeCounter_10)
    t2.start()
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
class login:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        if loginuser:
            return render.index(loginuser, namelistdata, poplistdata)
        else:
            return render.login('欢迎访问，请先登录...')
    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('passwd')
        if (username,passwd) in settings.allowed:
            loginuser = username
            web.setcookie('user_id', loginuser, settings.COOKIE_EXPIRES)
            return render.index(loginuser,namelistdata, poplistdata)
        else:
            return render.login('登录错误，请重新登陆...')
class logout:
    def GET(self):
        web.setcookie('user_id', loginuser, -1)
        return render.login('欢迎，请登录...')
class historical:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        if loginuser:
            return render.historical(loginuser, namelistdata, poplistdata)
        else:
            return render.login('欢迎，请登录...')
class data:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        if loginuser:
            return render.index(loginuser, namelistdata, poplistdata)
        else:
            return render.login('欢迎，请登录...')
if __name__ == '__main__':
   # X秒打印一次时间
    #TimeCounter_5()
    #TimeCounter_10()
   # X秒与Modbus主机通讯一次
    #ModBusCommunication(10)
   # 初始化对话框
    #ui = UIThread("UIThread")
    #ui.start()
    #mysql.start()
   # 启动web服务
    app.run()
