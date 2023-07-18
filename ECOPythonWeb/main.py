# -*- coding: utf-8 -*-
# filename: main.py
import web
import threading
import settings
import model
from datetime import datetime
from threading import Timer
from model import Handle
loginuser=''
web.config.debug = True
app = web.application(settings.urls, globals())
render = web.template.render('templates')
ColumnData = model.CurrentData.getColumnList()
ColumnList12 = dict(zip(ColumnData["column_name"], ColumnData["comments"]))
ColumnList3 = dict(zip(ColumnData["column_name"], ColumnData["comments_for_HL"]))
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
def TimeCounter_60():
    # 打印时间函数
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
    model.run_mysql()
    model.run_mysql_HL()
    #weixin.run_weixin()
    #weixin.repeat_weixin(1440)
    global t1
    t1 = Timer(60, TimeCounter_60)
    t1.start()
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
            i = web.input()
            if i.get('sn'):
                sn = int(i.get('sn'))
            else:
                sn=settings.auth[loginuser]
            if (sn==1)|(sn==2):
                return render.index12(loginuser, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn))
            elif sn==3:
                return render.index3(loginuser, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn))
            else:
                return None
        else:
            return render.login('欢迎访问，请先登录...')
    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('passwd')
        if (username,passwd) in settings.allowed:
            loginuser = username
            usertype = settings.auth[loginuser]
            web.setcookie('user_id', loginuser, settings.COOKIE_EXPIRES)
            if (loginuser == '111') | (loginuser == '222'):
                return render.index12(loginuser, model.CurrentData.getCurrentData(1), model.CurrentData.getPreData(1))
            elif loginuser == '333':
                return render.index3(loginuser, model.CurrentData.getCurrentData(3), model.CurrentData.getPreData(3))
            else:
                return render.login('登录错误，请重新登陆...')
        else:
            return render.login('登录错误，请重新登陆...')
class logout:
    def GET(self):
        web.setcookie('user_id', loginuser, -1)
        return render.login('欢迎，请登录...')
class historical:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        his_data = {
                    "TIMETAG":[202310011000, 202310011001, 202310011002, 202310011003, 202310011004, 202310011005, 202310011006], 
                    "result":[820, 932, 901, 934, 1290, 1330, 1320]
                    }
        if loginuser:
            if (loginuser=='111') | (loginuser=='222'):
                return render.historical(loginuser, ColumnList12, his_data)
            if loginuser=='333':
                return render.historical(loginuser, ColumnList3, his_data)
        else:
            return render.login('欢迎，请登录...')
    def POST(self):
        i = web.input()
        loginuser=web.cookies().get('user_id')
        startdatetime = i.get('date1') + ' ' +  i.get('time1') + ':00'
        enddatetime = i.get('date2') + ' ' + i.get('time2') + ':00'
        column_name = i.get('select')
        if loginuser:
            if (loginuser=='111') | (loginuser=='222'):
                if i.get('select2') == '鹤淇一号机组':
                    sn = 1
                elif i.get('select2') == '鹤淇二号机组':
                    sn = 2
                else:
                    sn = -1
                selected_column = list(ColumnList12.keys())[list(ColumnList12.values()).index(column_name)]
                his_data = model.CurrentData.getHisData(sn, selected_column, startdatetime, enddatetime)
                #show_data = dict(his_data['result'])
                return render.historical(loginuser, ColumnList12, his_data)
            if loginuser=='333':
                sn = 3
                selected_column = list(ColumnList3.keys())[list(ColumnList3.values()).index(column_name)]
                hisdata = model.CurrentData.getHisData(sn, selected_column, startdatetime, enddatetime)
                return render.historical(loginuser, ColumnList3, hisdata)
        else:
            return render.login('欢迎，请登录...')

if __name__ == '__main__':
    #model.conn_weixin()
    #TimeCounter_60()
    app.run()
