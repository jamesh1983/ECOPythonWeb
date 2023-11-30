# -*- coding: utf-8 -*-
# filename: main.py
import web
import threading
import settings
import model
import datetime
from threading import Timer
from model import Handle
loginuser=''
web.config.debug = True

app = web.application(settings.urls, globals())
render = web.template.render('templates')
ColumnData = model.CurrentData.getColumnList()
ColumnList12 = dict(zip(ColumnData["column_name"], ColumnData["comments"]))
ColumnList3 = dict(zip(ColumnData["column_name"], ColumnData["comments_for_HL"]))
ColumnList4 = dict(zip(ColumnData["column_name"], ColumnData["comments_for_GQ"]))
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
    #print('T1现在时间：',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    #print('T2现在时间：',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #具体触发内容
    ###
    #weixin.repeat_weixin(9)
    global t2
    t2 = Timer(10, TimeCounter_10)
    t2.start()
def TimeCounter_60():
    # 打印时间函数
    #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        #print ("开始线程：" + self.threadID)
        # 创建UI
        UIModule.ui_create()
        #root.mainloop()
        #print ("退出线程：" + self.threadID)

class login:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        if loginuser:
            i = web.input()
            if i.get('sn'):
                sn = int(i.get('sn'))
                if (i.get('dates') == '7'):
                    delta_day=datetime.timedelta(days=7)
                elif (i.get('dates') == '30'):
                    delta_day=datetime.timedelta(days=30)
                else:
                    delta_day=datetime.timedelta(days=1)
            else:
                sn=settings.auth[loginuser]
                delta_day=datetime.timedelta(days=1)
            s_day = datetime.datetime.today() - delta_day
            startdate = s_day.strftime("%Y-%m-%d")
            enddate = datetime.datetime.today().strftime("%Y-%m-%d")
            
            if sn==1:
                selected_column = "Value1"
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value2"
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value3"
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_1(loginuser,sn, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn), his_data_1, his_data_2, his_data_3, model.CurrentData.getPreDataZK(sn))
                #return render.index12(loginuser, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn))
            elif sn==2:
                selected_column = "Value1"
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value2"
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value3"
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_1(loginuser,sn, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn), his_data_1, his_data_2, his_data_3, model.CurrentData.getPreDataZK(sn))
            elif sn==3:
                selected_column = "int_8"
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "int_10"
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value5"
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_3(loginuser, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn), his_data_1, his_data_2, his_data_3)
            elif sn==4:
                selected_column = "bool37"#1号硝化液回流泵
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool39"#1号硝化液回流泵
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool19"#1号污泥回流泵
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool21"#2号污泥回流泵
                his_data_4 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_4(loginuser, model.CurrentData.getCurrentData(sn), his_data_1, his_data_2, his_data_3, his_data_4)
            else:
                return None
        else:
            return render.login_1("欢迎，请登录...")
    def POST(self):
        i = web.input()
        username = i.get('user_id')
        passwd = i.get('password')
        if (username,passwd) in settings.allowed:
            loginuser = username
            usertype = settings.auth[loginuser]
            web.setcookie('user_id', loginuser, settings.COOKIE_EXPIRES)
            oneday=datetime.timedelta(days=1)
            yesterday = datetime.datetime.today() - oneday
            startdate = yesterday.strftime("%Y-%m-%d")
            enddate = datetime.datetime.today().strftime("%Y-%m-%d")
            if (loginuser == '111') | (loginuser == '222'):
                sn = 1
                selected_column = "Value1"#进水水温
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value2"#出水水温
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value3"#端差
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_1(loginuser,sn, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn), his_data_1, his_data_2, his_data_3, model.CurrentData.getPreDataZK(sn))
                #return render.index12(loginuser, model.CurrentData.getCurrentData(1), model.CurrentData.getPreData(1))
            elif loginuser == '333':
                sn = 3
                selected_column = "int_8"#ORP1
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "int_10"#ORP2
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "Value5"#进水水温
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_3(loginuser, model.CurrentData.getCurrentData(sn), model.CurrentData.getPreData(sn), his_data_1, his_data_2, his_data_3)
            elif loginuser == '444':
                sn = 4
                selected_column = "bool37"#1号硝化液回流泵
                his_data_1 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool39"#2号硝化液回流泵
                his_data_2 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool19"#1号污泥回流泵
                his_data_3 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                selected_column = "bool21"#2号污泥回流泵
                his_data_4 = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.index_4(loginuser, model.CurrentData.getCurrentData(sn), his_data_1, his_data_2, his_data_3, his_data_4)
            else:
                return render.login_1("登录错误，请重新登录...")
        else:
            return render.login_1("登录错误，请重新登录...")
class logout:
    def GET(self):
        web.setcookie('user_id', loginuser, -1)
        return render.login_1("欢迎，请登录...")
class historical:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        if loginuser:
            oneday=datetime.timedelta(days=1)
            yesterday = datetime.datetime.today() - oneday
            startdate = yesterday.strftime("%Y-%m-%d")
            enddate = datetime.datetime.today().strftime("%Y-%m-%d")
            if (loginuser=='111') | (loginuser=='222'):
                sn = 1
                selected_column = "Value8"
                his_data = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.historical_1(loginuser, ColumnList12, his_data, "凝汽器前ORP")
            if loginuser=='333':
                sn = 3
                selected_column = "int_8"
                his_data = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.historical_1(loginuser, ColumnList3, his_data, "凝汽器前ORP值1")
            if loginuser=='444':
                sn = 4
                selected_column = "bool1"
                his_data = model.CurrentData.getHisData(sn, selected_column, startdate, enddate)
                return render.historical_1(loginuser, ColumnList4, his_data, "调节池低液位")
        else:
            return render.login_1('欢迎，请登录...')
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
                tilte_name = i.get('select2')+"-"+column_name
                return render.historical_1(loginuser, ColumnList12, his_data, tilte_name)
            if loginuser=='333':
                sn = 3
                selected_column = list(ColumnList3.keys())[list(ColumnList3.values()).index(column_name)]
                hisdata = model.CurrentData.getHisData(sn, selected_column, startdatetime, enddatetime)
                tilte_name = column_name
                return render.historical_1(loginuser, ColumnList3, hisdata, tilte_name)
            if loginuser=='444':
                sn = 4
                selected_column = list(ColumnList4.keys())[list(ColumnList4.values()).index(column_name)]
                hisdata = model.CurrentData.getHisData(sn, selected_column, startdatetime, enddatetime)
                tilte_name = column_name
                return render.historical_1(loginuser, ColumnList4, hisdata, tilte_name)
        else:
            return render.login('欢迎，请登录...')
class calendar:
    def GET(self):
        loginuser=web.cookies().get('user_id')
        return render.calendar_1(loginuser)
if __name__ == '__main__':
    #TimeCounter_60()
    #model.conn_weixin()
    app.run()
